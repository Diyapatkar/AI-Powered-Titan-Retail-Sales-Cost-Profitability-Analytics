CREATE DATABASE Titan_Retail_Analytics;
USE Titan_Retail_Analytics;

SELECT TOP 10 * FROM Titan_Retail;

SELECT COUNT(*) AS Total_Records FROM Titan_Retail;

-- SQL analysis
SELECT COUNT(*) AS Total_Records FROM Titan_Retail;

-- Order status distribution
SELECT Order_Status,
	COUNT(*) AS Total_Orders
FROM Titan_Retail
GROUP BY Order_Status
ORDER BY Total_Orders DESC;

-- Category-wise revenue and profit
SELECT Product_Category,
	SUM(Net_Revenue_INR) AS Revenue,
	SUM(Gross_Profit_INR) AS Profit,
	SUM(Total_Cost_INR) AS Total_Cost
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Product_Category
ORDER BY Profit DESC;

-- Region-wise performance
SELECT 
	Region,
	SUM(Net_Revenue_INR) AS REVENUE,
	SUM(Gross_Profit_INR) AS PROFIT,
	SUM(Total_Cost_INR) AS COST
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Region
ORDER BY PROFIT DESC;

-- Sales channel performance
SELECT 
	Sales_Channel,
	COUNT(*) AS Total_Orders,
	SUM(Net_Revenue_INR) as Revenue,
	SUM(Gross_Profit_INR) as Profit
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY Sales_Channel
ORDER BY Profit DESC;

-- Monthly revenue trend
SELECT 
	YEAR(Order_Date) AS Sales_Year,
	MONTH(Order_Date) AS Sales_Month,
	SUM(Net_Revenue_INR) AS Revenue,
	SUM(Gross_Profit_INR) AS Profit
FROM Titan_Retail
WHERE Order_Status = 'Delivered'
GROUP BY YEAR(Order_Date), MONTH(Order_Date)
ORDER BY Sales_Year, Sales_Month;

