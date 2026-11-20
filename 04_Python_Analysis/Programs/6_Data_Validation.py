# Load data
import pandas as pd

df = pd.read_csv(
    r"C:\Users\diyap\OneDrive\ドキュメント\Data Analytics\AI Powered Titan Retail Sales & Profitability Analytics\01_Data\Cleaned_Data\Titan_Retail_Cleaned_Master.csv"
)

sales = df[df["Order_Status"] == "Delivered"].copy()

print("Total records:", len(df))
print("Delivered records:", len(sales))

# Calculate final KPIs
kpis = {
    "Total Orders": sales["Order_ID"].nunique(),
    "Total Quantity": sales["Quantity"].sum(),
    "Total Revenue": sales["Net_Revenue_INR"].sum(),
    "Total Cost": sales["Total_Cost_INR"].sum(),
    "Total Profit": sales["Gross_Profit_INR"].sum(),
    "Profit Margin %": (
        sales["Gross_Profit_INR"].sum()
        / sales["Net_Revenue_INR"].sum()
    ) * 100,
    "Average Order Value": (
        sales["Net_Revenue_INR"].sum()
        / sales["Order_ID"].nunique()
    )
}

kpi_df = pd.DataFrame(
    list(kpis.items()),
    columns=["KPI", "Python Value"]
)

print(kpi_df)

# Financial validation
sales["Calculated_Profit"] = (
    sales["Net_Revenue_INR"] - sales["Total_Cost_INR"]
)

sales["Profit_Check"] = (
    sales["Gross_Profit_INR"].round(2)
    == sales["Calculated_Profit"].round(2)
)

print("Profit calculation errors:", (~sales["Profit_Check"]).sum())

print(
    "Cost calculation errors:",
    (
        sales["Total_Cost_INR"].round(2)
        != (
            sales["Product_Cost_INR"] +
            sales["Shipping_Cost_INR"]
        ).round(2)
    ).sum()
)

# Export validation results
output_path = (
    r"C:\Users\diyap\OneDrive\ドキュメント\Data Analytics\AI Powered Titan Retail Sales & Profitability Analytics\07_Reports\KPI_Cross_Validation.xlsx"
)

kpi_df.to_excel(output_path, index=False)

print("Validation report exported successfully!")

