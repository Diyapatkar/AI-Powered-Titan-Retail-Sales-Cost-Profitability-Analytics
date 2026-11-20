-- Business Insights - 1

-- Top 10 profitable products
SELECT TOP 10
	Product_Name,
	SUM(Net_Revenue_INR) AS REVENUE,
	SUM(Gross_Profit_INR) AS PROFIT
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Product_Name
ORDER BY PROFIT DESC;

--Profit margin by category
SELECT
    Product_Category,
    SUM(Net_Revenue_INR) AS Revenue,
    SUM(Gross_Profit_INR) AS Profit,
    CAST(
        100.0 * SUM(Gross_Profit_INR) /
        (SUM(Net_Revenue_INR))
        AS DECIMAL(10,2)
    ) AS Profit_Margin_Percent
FROM dbo.Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Product_Category
ORDER BY Profit_Margin_Percent DESC;

-- Discount impact on profitability
SELECT
    CASE
        WHEN Discount_Percent = 0 THEN 'No Discount'
        WHEN Discount_Percent <= 10 THEN '1-10%'
        WHEN Discount_Percent <= 20 THEN '11-20%'
        ELSE 'Above 20%'
    END AS Discount_Group,
    COUNT(*) AS Orders,
    SUM(Net_Revenue_INR) AS Revenue,
    SUM(Gross_Profit_INR) AS Profit
FROM dbo.Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY
    CASE
        WHEN Discount_Percent = 0 THEN 'No Discount'
        WHEN Discount_Percent <= 10 THEN '1-10%'
        WHEN Discount_Percent <= 20 THEN '11-20%'
        ELSE 'Above 20%'
    END
ORDER BY Profit DESC;

-- Top 10 customers by revenue
SELECT 
    TOP 10 Customer_ID,
    SUM(Net_Revenue_INR) AS REVENUE,
    SUM(Gross_Profit_INR) AS PROFIT
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Customer_ID
ORDER BY REVENUE DESC;



-- BUSINESS INSIGHTS - 2

-- Products earning above average product profit
SELECT
    Product_Name,
    SUM(Gross_Profit_INR) AS Total_Profit
FROM dbo.Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Product_Name
HAVING SUM(Gross_Profit_INR) >
(
    SELECT AVG(Product_Profit)
    FROM
    (
        SELECT
            SUM(Gross_Profit_INR) AS Product_Profit
        FROM dbo.Titan_Retail
        WHERE Order_Status = 'Delivered'
        GROUP BY Product_Name
    ) AS P
)
ORDER BY Total_Profit DESC;

-- CTE – Category performance
WITH CategorySales AS
(
    SELECT 
        Product_Category,
        SUM(Net_Revenue_INR) AS REVENUE,
        SUM(Gross_Profit_INR) AS PROFIT
    FROM Titan_Retail
    WHERE Order_Status = 'Delivered'
    GROUP BY Product_Category
)

SELECT 
    Product_Category,
    REVENUE,
    PROFIT,
    CAST(
        100.0 * PROFIT / REVENUE AS decimal(10,2)
    ) AS PROFIT_MARGIN
FROM CategorySales
ORDER BY PROFIT DESC;

-- Rank categories by profit
SELECT 
    Product_Category,
    SUM(Gross_Profit_INR) AS PROFIT,
    DENSE_RANK() OVER (
        ORDER BY SUM(Gross_Profit_INR) DESC
    ) AS PROFIT_RANK
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Product_Category 
ORDER BY PROFIT

-- Month-over-month revenue comparison
WITH MonthlySales AS
(
    SELECT
        DATEFROMPARTS(
            YEAR(Order_Date),
            MONTH(Order_Date),
            1
        ) AS Sales_Month,
        SUM(Net_Revenue_INR) AS Revenue
    FROM dbo.Titan_Retail
    WHERE Order_Status = 'Delivered'
    GROUP BY
        YEAR(Order_Date),
        MONTH(Order_Date)
),
PreviousMonth AS
(
    SELECT
        Sales_Month,
        Revenue,
        LAG(Revenue) OVER (
            ORDER BY Sales_Month
        ) AS Previous_Revenue
    FROM MonthlySales
)
SELECT
    Sales_Month,
    Revenue,
    Previous_Revenue,
    CAST(
        100.0 * (Revenue - Previous_Revenue) /
        NULLIF(Previous_Revenue, 0)
        AS DECIMAL(10,2)
    ) AS Growth_Percent
FROM PreviousMonth
ORDER BY Sales_Month;

-- Running total of monthly revenue
WITH MonthlySales AS
(
    SELECT
        DATEFROMPARTS(
            YEAR(Order_Date),
            MONTH(Order_Date),
            1
        ) AS Sales_Month,
        SUM(Net_Revenue_INR) AS Revenue
    FROM dbo.Titan_Retail
    WHERE Order_Status = 'Delivered'
    GROUP BY YEAR(Order_Date), MONTH(Order_Date)
)
SELECT
    Sales_Month,
    Revenue,
    SUM(Revenue) OVER (
        ORDER BY Sales_Month
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS Running_Revenue
FROM MonthlySales
ORDER BY Sales_Month;