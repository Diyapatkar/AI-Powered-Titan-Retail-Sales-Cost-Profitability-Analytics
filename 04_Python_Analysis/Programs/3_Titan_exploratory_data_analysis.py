# Import libraries and load dataset
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "01_Data"
    / "Cleaned_Data"
    / "Titan_Retail_Cleaned_Master.csv"
)

if not DATA_PATH.is_file():
    raise FileNotFoundError(
        f"Dataset not found at {DATA_PATH}. Check that the cleaned CSV exists."
    )

df = pd.read_csv(DATA_PATH)

if "Order_Date" not in df.columns:
    raise KeyError("The dataset does not contain the required 'Order_Date' column.")

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nFirst five rows:")
print(df.head())

print("\nMissing values by column:")
print(df.isna().sum())

print("\nColumn data types:")
print(df.dtypes)

# Prepare analysis dataset 
sales = df[df["Order_Status"] == "Delivered"].copy()

print("Total Records:", len(df))
print("Delivered Records:", len(sales))
print("Revenue:", sales["Net_Revenue_INR"].sum())
print("Profit:", sales["Gross_Profit_INR"].sum())

# Overall business performance
total_revenue = sales["Net_Revenue_INR"].sum()
total_cost = sales["Total_Cost_INR"].sum()
total_profit = sales["Gross_Profit_INR"].sum()
total_orders = sales["Order_ID"].nunique()
total_quantity = sales["Quantity"].sum()

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue else 0
)

print("Total Orders:", total_orders)
print("Total Quantity:", total_quantity)
print("Total Revenue: ₹", round(total_revenue, 2))
print("Total Cost: ₹", round(total_cost, 2))
print("Total Profit: ₹", round(total_profit, 2))
print("Profit Margin:", round(profit_margin, 2), "%")

# Category performance analysis
category = sales.groupby("Product_Category").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Cost=("Total_Cost_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Quantity=("Quantity", "sum")
).reset_index()

category["Profit_Margin"] = (
    category["Profit"] / category["Revenue"] * 100
)

category = category.sort_values(
    "Profit", ascending=False
)

print(category)


plt.figure(figsize=(10,5))

plt.bar(
    category["Product_Category"],
    category["Profit"]
)

plt.title("Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Profit (INR)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# Regional Performance
region = sales.groupby("Region").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index().sort_values(
    "Revenue", ascending=False
)

print(region)

plt.figure(figsize=(8,5))

plt.bar(region["Region"], region["Revenue"])

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (INR)")
plt.tight_layout()
plt.show()

# Monthly sales trend
sales["Order_Month"] = (
    sales["Order_Date"].dt.to_period("M")
)

monthly = sales.groupby("Order_Month").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index()

monthly["Order_Month"] = (
    monthly["Order_Month"].astype(str)
)

print(monthly)

plt.figure(figsize=(14,5))

plt.plot(
    monthly["Order_Month"],
    monthly["Revenue"],
    marker="o",
    label="Revenue"
)

plt.plot(
    monthly["Order_Month"],
    monthly["Profit"],
    marker="o",
    label="Profit"
)

plt.title("Monthly Revenue and Profit Trend")
plt.xlabel("Month")
plt.ylabel("Amount (INR)")
plt.xticks(rotation=60)
plt.legend()
plt.tight_layout()
plt.show()

# Top 10 profitable products
products = sales.groupby("Product_Name").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Quantity=("Quantity", "sum")
).reset_index()

top_products = products.sort_values(
    "Profit", ascending=False
).head(10)

print(top_products)

plt.figure(figsize=(10,6))

plt.barh(
    top_products["Product_Name"],
    top_products["Profit"]
)

plt.title("Top 10 Products by Profit")
plt.xlabel("Profit (INR)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

#Discount impact analysis
sales["Discount_Group"] = pd.cut(
    sales["Discount_Percent"],
    bins=[-0.01, 0, 10, 20, 100],
    labels=[
        "No Discount",
        "1-10%",
        "11-20%",
        "Above 20%"
    ]
)

discount_analysis = sales.groupby(
    "Discount_Group",
    observed=False
).agg(
    Orders=("Order_ID", "count"),
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index()

print(discount_analysis)

plt.figure(figsize=(8,5))

plt.bar(
    discount_analysis["Discount_Group"].astype(str),
    discount_analysis["Profit"]
)

plt.title("Profit by Discount Group")
plt.xlabel("Discount")
plt.ylabel("Profit (INR)")
plt.tight_layout()
plt.show()

# Customer analysis
customers = sales.groupby("Customer_ID").agg(
    Orders=("Order_ID", "nunique"),
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index()

top_customers = customers.sort_values(
    "Revenue", ascending=False
).head(10)

print(top_customers)

# Sales channel analysis
channel = sales.groupby("Sales_Channel").agg(
    Orders=("Order_ID", "count"),
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum")
).reset_index()

print(channel)

# Find unusual profit records
Q1 = sales["Gross_Profit_INR"].quantile(0.25)
Q3 = sales["Gross_Profit_INR"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = sales[
    (sales["Gross_Profit_INR"] < lower) |
    (sales["Gross_Profit_INR"] > upper)
]

print("Potential unusual records:", len(outliers))

print(
    outliers[
        ["Order_ID", "Product_Name",
         "Net_Revenue_INR", "Gross_Profit_INR"]
    ].head(10)
)

# Export analysis results
output_dir = Path(__file__).resolve().parent
output_dir.mkdir(parents=True, exist_ok=True)

category.to_csv(output_dir / "Category_Analysis.csv", index=False)
region.to_csv(output_dir / "Regional_Analysis.csv", index=False)
monthly.to_csv(output_dir / "Monthly_Analysis.csv", index=False)
top_products.to_csv(output_dir / "Top_Products.csv", index=False)
discount_analysis.to_csv(output_dir / "Discount_Analysis.csv", index=False)
top_customers.to_csv(output_dir / "Top_Customers.csv", index=False)