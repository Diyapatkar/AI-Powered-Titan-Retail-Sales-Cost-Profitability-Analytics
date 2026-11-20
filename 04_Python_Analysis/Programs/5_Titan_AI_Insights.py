# Load analysis data
import pandas as pd
import numpy as np

df = pd.read_csv(
    r"C:\Users\diyap\OneDrive\ドキュメント\Data Analytics\AI Powered Titan Retail Sales & Profitability Analytics\01_Data\Cleaned_Data\Titan_Retail_Cleaned_Master.csv"
)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

sales = df[df["Order_Status"] == "Delivered"].copy()

print("Delivered records:", len(sales))

# Generate a business performance summary
revenue = sales["Net_Revenue_INR"].sum()
cost = sales["Total_Cost_INR"].sum()
profit = sales["Gross_Profit_INR"].sum()

business_summary = {
    "Total_Orders": int(sales["Order_ID"].nunique()),
    "Total_Quantity": int(sales["Quantity"].sum()),
    "Revenue_INR": round(revenue, 2),
    "Cost_INR": round(cost, 2),
    "Profit_INR": round(profit, 2),
    "Profit_Margin_Percent": round(profit / revenue * 100, 2)
}

print(business_summary)

# Generate category-level AI insights
category_summary = sales.groupby("Product_Category").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Cost=("Total_Cost_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Orders=("Order_ID", "count")
).reset_index()

category_summary["Profit_Margin_Percent"] = (
    category_summary["Profit"] /
    category_summary["Revenue"] * 100
)

category_summary = category_summary.sort_values(
    "Profit", ascending=False
)

print(category_summary.round(2))

# Generate regional insights
region_summary = sales.groupby("Region").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Orders=("Order_ID", "count")
).reset_index()

region_summary["Profit_Margin_Percent"] = (
    region_summary["Profit"] /
    region_summary["Revenue"] * 100
)

print(region_summary.round(2))

# Generate monthly business insights
monthly_summary = sales.groupby(
    sales["Order_Date"].dt.to_period("M")
).agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index()

monthly_summary["Month"] = (
    monthly_summary["Order_Date"].astype(str)
)

monthly_summary["Revenue_Growth_Percent"] = (
    monthly_summary["Revenue"].pct_change() * 100
)

print(monthly_summary.round(2))

# Create an AI input file automatically
import json

ai_input = {
    "Business_Performance": business_summary,
    "Category_Analysis": category_summary.round(2).to_dict("records"),
    "Regional_Analysis": region_summary.round(2).to_dict("records"),
    "Monthly_Analysis": monthly_summary.round(2).to_dict("records")
}

with open(
    "Titan_AI_Analysis_Input.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(ai_input, file, indent=4, default=str)

print("AI input file created!")

# Create an automated monthly report
latest = monthly_summary.iloc[-1]

previous = monthly_summary.iloc[-2]

report = f"""
# Titan Retail Monthly Business Report

## Latest Month: {latest['Month']}

- Revenue: ₹{latest['Revenue']:,.2f}
- Profit: ₹{latest['Profit']:,.2f}
- Revenue Growth: {latest['Revenue_Growth_Percent']:.2f}%

## Previous Month Comparison

- Previous Revenue: ₹{previous['Revenue']:,.2f}
- Current Revenue: ₹{latest['Revenue']:,.2f}

## Category Performance

{category_summary.to_markdown(index=False)}

## Regional Performance

{region_summary.to_markdown(index=False)}

---
Dataset: Simulated Titan-inspired retail transactions.
"""

with open(
    "Monthly_Business_Report.md",
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

print("Monthly report generated!")
