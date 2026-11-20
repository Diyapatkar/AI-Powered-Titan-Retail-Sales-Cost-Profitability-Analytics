-- Data validation

-- Check duplicate Order IDs
SELECT 
    Order_ID,
    COUNT(*) AS Duplicate_Count
FROM Titan_Retail
GROUP BY Order_ID
HAVING COUNT(*) > 1;

-- Compare order statuses
SELECT
    Order_Status,
    COUNT(*) AS Orders,
    SUM(Net_Revenue_INR) AS Revenue,
    SUM(Gross_Profit_INR) AS Profit
FROM dbo.Titan_Retail
GROUP BY Order_Status
ORDER BY Orders DESC;