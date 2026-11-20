import pandas as pd
import numpy as np
from pathlib import Path

#Load dataset
file_path = (
    Path(__file__).resolve().parent.parent
    / "01_Data"
    / "Titan_Inspired_Retail_Analytics_12000_Records.csv"
)

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)

df.head()

# Data quality checks
# Check for missing values
missing = df.isnull().sum()
print(missing[missing > 0])
print("Total missing values:", df.isnull().sum().sum())

# Check for duplicate records
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Order IDs:", df["Order_ID"].duplicated().sum())

#C. Data types
df.info()

#D. Date validation
df["Order_Date"] = pd.to_datetime(    df["Order_Date"], errors="coerce")
print("Invalid dates:", df["Order_Date"].isnull().sum())
print("Date range:", df["Order_Date"].min(),      "to", df["Order_Date"].max())

# E. Invalid numerical values
print("Negative Quantity:", (df["Quantity"] < 0).sum())
print("Negative Selling Price:",      (df["Unit_Selling_Price_INR"] < 0).sum())
print("Invalid Discount:",      (~df["Discount_Percent"].between(0, 100)).sum())
print("Invalid Profit Margin:",      (~df["Profit_Margin_Percent"].between(-100, 100)).sum())

# Financial calculation validation
df["Revenue_Check"] = (
    df["Gross_Revenue_INR"] -
    df["Discount_Amount_INR"]
)

df["Cost_Check"] = (
    df["Product_Cost_INR"] +
    df["Shipping_Cost_INR"]
)

df["Profit_Check"] = (
    df["Net_Revenue_INR"] -
    df["Total_Cost_INR"]
)

print("Revenue errors:",
      (df["Revenue_Check"] - df["Net_Revenue_INR"]).abs().gt(0.02).sum())

print("Cost errors:",
      (df["Cost_Check"] - df["Total_Cost_INR"]).abs().gt(0.02).sum())

print("Profit errors:",
      (df["Profit_Check"] - df["Gross_Profit_INR"]).abs().gt(0.02).sum())

# Business-rule validation
status_analysis = df.groupby("Order_Status").agg(
    Orders=("Order_ID", "count"),
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
)

status_analysis

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

delivered_df = df[
    df["Order_Status"] == "Delivered"
].copy()

print("Master records:", len(df))
print("Delivered records:", len(delivered_df))

# Create useful calculated columns
df["Order_Month"] = df["Order_Date"].dt.month_name()

df["Order_Year"] = df["Order_Date"].dt.year

df["Order_Year_Month"] = (
    df["Order_Date"].dt.to_period("M").astype(str)
)

df["Cost_Per_Unit"] = (
    df["Total_Cost_INR"] / df["Quantity"]
)

df["Profit_Per_Unit"] = (
    df["Gross_Profit_INR"] / df["Quantity"]
)

df.head()

# Export cleaned datasets
output_path = Path(__file__).resolve().parent.parent / "01_Data" / "Cleaned_Data"
output_path.mkdir(parents=True, exist_ok=True)

df.to_csv(
    output_path / "Titan_Retail_Cleaned_Master.csv",
    index=False
)

delivered_df.to_csv(
    output_path / "Titan_Retail_Delivered_Only.csv",
    index=False
)

print("Cleaned datasets exported successfully!")

# Generate a data quality report
quality_report = pd.DataFrame({
    "Check": [
        "Total Rows",
        "Total Columns",
        "Missing Values",
        "Duplicate Rows",
        "Duplicate Order IDs",
        "Invalid Dates",
        "Negative Quantities"
    ],
    "Result": [
        len(df),
        len(df.columns),
        df.isnull().sum().sum(),
        df.duplicated().sum(),
        df["Order_ID"].duplicated().sum(),
        df["Order_Date"].isnull().sum(),
        (df["Quantity"] < 0).sum()
    ]
})

quality_report

quality_report.to_excel(
    output_path / "Data_Quality_Report.xlsx",
    index=False
)