# Load the dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"C:\Users\diyap\OneDrive\ドキュメント\Data Analytics\AI Powered Titan Retail Sales & Profitability Analytics\01_Data\Cleaned_Data\Titan_Retail_Cleaned_Master.csv"
)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

sales = df[df["Order_Status"] == "Delivered"].copy()

print(sales.shape)

# Month-over-month growth analysis
monthly = (
    sales.groupby(sales["Order_Date"].dt.to_period("M"))
    .agg(
        Revenue=("Net_Revenue_INR", "sum"),
        Profit=("Gross_Profit_INR", "sum")
    )
    .reset_index()
)

monthly["Month"] = monthly["Order_Date"].astype(str)

monthly["Revenue_Growth_%"] = (
    monthly["Revenue"].pct_change() * 100
)

monthly["Profit_Growth_%"] = (
    monthly["Profit"].pct_change() * 100
)

print(monthly.round(2))

plt.figure(figsize=(13,5))
plt.plot(monthly["Month"], monthly["Revenue_Growth_%"], marker="o")
plt.axhline(0, linestyle="--")
plt.title("Monthly Revenue Growth (%)")
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()

# Profitability analysis
category_profit = sales.groupby("Product_Category").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Cost=("Total_Cost_INR", "sum")
).reset_index()

category_profit["Profit_Margin_%"] = (
    category_profit["Profit"] /
    category_profit["Revenue"] * 100
)

print(category_profit.round(2))

plt.figure(figsize=(9,6))

plt.scatter(
    category_profit["Revenue"],
    category_profit["Profit_Margin_%"],
    s=120
)

for _, row in category_profit.iterrows():
    plt.annotate(
        row["Product_Category"],
        (row["Revenue"], row["Profit_Margin_%"])
    )

plt.title("Revenue vs Profit Margin by Category")
plt.xlabel("Revenue (INR)")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()
plt.show()

# Discount and profitability relationship
discount = sales.groupby("Discount_Percent").agg(
    Revenue=("Net_Revenue_INR", "sum"),
    Profit=("Gross_Profit_INR", "sum"),
    Orders=("Order_ID", "count")
).reset_index()

discount["Profit_Margin_%"] = (
    discount["Profit"] / discount["Revenue"] * 100
)

print(discount.head(15).round(2))

correlation = sales[
    ["Discount_Percent", "Profit_Margin_Percent"]
].corr()

print(correlation)

# Customer segmentation – RFM Analysis
reference_date = sales["Order_Date"].max() + pd.Timedelta(days=1)

rfm = sales.groupby("Customer_ID").agg(
    Last_Purchase=("Order_Date", "max"),
    Frequency=("Order_ID", "nunique"),
    Monetary=("Net_Revenue_INR", "sum")
).reset_index()

rfm["Recency"] = (
    reference_date - rfm["Last_Purchase"]
).dt.days

print(rfm.head())

rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

print(rfm.head(10))

rfm["Customer_Segment"] = np.select(
    [
        (rfm["R_Score"] >= 3) & (rfm["F_Score"] >= 3),
        (rfm["R_Score"] <= 2) & (rfm["F_Score"] >= 3),
        (rfm["R_Score"] >= 3) & (rfm["F_Score"] <= 2)
    ],
    [
        "Loyal Customers",
        "At Risk Loyal Customers",
        "New or Promising Customers"
    ],
    default="Other Customers"
)

print(
    rfm["Customer_Segment"].value_counts().reset_index()
)

# Statistical analysis
print("Mean Profit:", sales["Gross_Profit_INR"].mean())
print("Median Profit:", sales["Gross_Profit_INR"].median())
print("Standard Deviation:", sales["Gross_Profit_INR"].std())
print("Minimum Profit:", sales["Gross_Profit_INR"].min())
print("Maximum Profit:", sales["Gross_Profit_INR"].max())

plt.figure(figsize=(9,5))

plt.hist(
    sales["Gross_Profit_INR"],
    bins=40
)

plt.title("Distribution of Transaction Profit")
plt.xlabel("Profit (INR)")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.show()

# Basic sales forecasting baseline
forecast_data = monthly[["Month", "Revenue"]].copy()

forecast_data["Moving_Average_3M"] = (
    forecast_data["Revenue"]
    .rolling(window=3)
    .mean()
)

print(forecast_data.tail(8))

plt.figure(figsize=(13,5))

plt.plot(
    forecast_data["Month"],
    forecast_data["Revenue"],
    label="Actual Revenue"
)

plt.plot(
    forecast_data["Month"],
    forecast_data["Moving_Average_3M"],
    label="3-Month Moving Average"
)

plt.title("Revenue Trend and Moving Average")
plt.xticks(rotation=60)
plt.legend()
plt.tight_layout()
plt.show()

# AI-powered business insights
summary = {
    "Total_Revenue": round(sales["Net_Revenue_INR"].sum(), 2),
    "Total_Profit": round(sales["Gross_Profit_INR"].sum(), 2),
    "Profit_Margin": round(
        sales["Gross_Profit_INR"].sum() /
        sales["Net_Revenue_INR"].sum() * 100, 2
    ),
    "Top_Category": category_profit.sort_values(
        "Profit", ascending=False
    ).iloc[0]["Product_Category"],
    "Top_Region": sales.groupby("Region")[
        "Net_Revenue_INR"
    ].sum().idxmax()
}

print(summary)

output = r"C:\Users\diyap\OneDrive\ドキュメント\Data Analytics\AI Powered Titan Retail Sales & Profitability Analytics\04_Python_Analysis"

monthly.to_csv(output + r"\Monthly_Growth_Analysis.csv", index=False)

category_profit.to_csv(
    output + r"\Category_Profitability.csv", index=False
)

rfm.to_csv(output + r"\Customer_RFM_Analysis.csv", index=False)

forecast_data.to_csv(
    output + r"\Revenue_Moving_Average.csv", index=False
)