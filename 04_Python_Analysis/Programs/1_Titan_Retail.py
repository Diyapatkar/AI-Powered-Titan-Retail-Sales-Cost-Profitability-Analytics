import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_path = (
    Path(__file__).resolve().parent.parent
    / "01_Data"
    / "Titan_Inspired_Retail_Analytics_12000_Records.csv"
)
df = pd.read_csv(data_path)
print("Dataset loaded successfully!")

# Dataset Dimensions    
print("Rows: ", df.shape[0])
print("Columns: ", df.shape[1])

# First five records
print("First five records:")
print(df.head())
print("\nDataset Info:")
df.info()
df.describe(include="all")

# Missing values
print("Missing values:",df.isnull().sum())

# Duplicate records
print("Duplicate rows:", df.duplicated().sum())

# Check date range
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
print("Start:", df["Order_Date"].min())
print("End:", df["Order_Date"].max())

# Revenue verification
df["Check_Revenue"] = (
    df["Gross_Revenue_INR"] -
    df["Discount_Amount_INR"]
)

# Cost verification
df["Check_Cost"] = (
    df["Product_Cost_INR"] +
    df["Shipping_Cost_INR"]
)

# Profit verification
df["Check_Profit"] = (
    df["Net_Revenue_INR"] -
    df["Total_Cost_INR"]
)

print("Revenue errors:",
      (df["Check_Revenue"] - df["Net_Revenue_INR"]).abs().gt(0.02).sum())

print("Cost errors:",
      (df["Check_Cost"] - df["Total_Cost_INR"]).abs().gt(0.02).sum())

print("Profit errors:",
      (df["Check_Profit"] - df["Gross_Profit_INR"]).abs().gt(0.02).sum())