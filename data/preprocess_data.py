import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Set2')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Create directories if they don't exist
os.makedirs('../images', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)

print("Loading raw data...")
# Load the sales data
sales_data = pd.read_csv('raw/sales_inventory_data.csv')
product_data = pd.read_csv('raw/product_data.csv')
store_data = pd.read_csv('raw/store_data.csv')

# Convert date column to datetime
sales_data['Date'] = pd.to_datetime(sales_data['Date'])

# Display basic information
print(f"Dataset shape: {sales_data.shape}")
print(f"Date range: {sales_data['Date'].min()} to {sales_data['Date'].max()}")
print(f"Number of products: {sales_data['Product_ID'].nunique()}")
print(f"Number of stores: {sales_data['Store_ID'].nunique()}")

# Merge with product and store data
sales_data = sales_data.merge(product_data, on='Product_ID', how='left')
sales_data = sales_data.merge(store_data, on='Store_ID', how='left')

# Extract date features
sales_data['Year'] = sales_data['Date'].dt.year
sales_data['Month'] = sales_data['Date'].dt.month
sales_data['Day'] = sales_data['Date'].dt.day
sales_data['DayOfWeek'] = sales_data['Date'].dt.dayofweek
sales_data['Quarter'] = sales_data['Date'].dt.quarter
sales_data['WeekOfYear'] = sales_data['Date'].dt.isocalendar().week

# Create a flag for weekends
sales_data['IsWeekend'] = sales_data['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

# Aggregate data to weekly level for time series forecasting
print("Aggregating data to weekly level...")
weekly_data = sales_data.groupby(['Year', 'WeekOfYear', 'Product_ID', 'Store_ID', 'Category', 'Region'])[
    ['Sales_Quantity', 'Inventory_Level', 'Price', 'Cost']
].agg({
    'Sales_Quantity': 'sum',
    'Inventory_Level': 'mean',
    'Price': 'mean',
    'Cost': 'mean'
}).reset_index()

# Create a date column for the week
weekly_data['Week_Start'] = weekly_data.apply(
    lambda row: pd.to_datetime(f"{row['Year']}-W{row['WeekOfYear']:02d}-1", format='%Y-W%W-%w'),
    axis=1
)

# Create lag features for each product-store combination
print("Creating lag features...")
def create_lag_features(group, lags=[1, 2, 3, 4]):
    for lag in lags:
        group[f'Sales_Lag_{lag}'] = group['Sales_Quantity'].shift(lag)
    return group

# Apply the function to each product-store group
weekly_with_lags = weekly_data.sort_values(['Product_ID', 'Store_ID', 'Week_Start']).groupby(['Product_ID', 'Store_ID']).apply(create_lag_features).reset_index(drop=True)

# Create rolling mean features
print("Creating rolling mean features...")
def create_rolling_features(group, windows=[2, 4, 8]):
    for window in windows:
        group[f'Sales_Rolling_{window}'] = group['Sales_Quantity'].shift(1).rolling(window=window, min_periods=1).mean()
    return group

# Apply the function to each product-store group
weekly_features = weekly_with_lags.sort_values(['Product_ID', 'Store_ID', 'Week_Start']).groupby(['Product_ID', 'Store_ID']).apply(create_rolling_features).reset_index(drop=True)

# Calculate inventory turnover
weekly_features['Inventory_Turnover'] = weekly_features['Sales_Quantity'] / weekly_features['Inventory_Level'].replace(0, 1)

# Calculate gross margin
weekly_features['Gross_Margin'] = (weekly_features['Price'] - weekly_features['Cost']) * weekly_features['Sales_Quantity']

# Drop rows with NaN values (first few weeks for each product-store combination)
weekly_features = weekly_features.dropna()

# Save the processed data
print("Saving processed data...")
weekly_features.to_csv('processed/weekly_data.csv', index=False)

# Split the data into training and testing sets
print("Splitting data into train and test sets...")
# Sort by date
weekly_features = weekly_features.sort_values('Week_Start')

# Determine the split point (use the last 8 weeks for testing)
split_date = weekly_features['Week_Start'].max() - pd.Timedelta(weeks=8)

# Split the data
train_data = weekly_features[weekly_features['Week_Start'] <= split_date]
test_data = weekly_features[weekly_features['Week_Start'] > split_date]

print(f"Training data shape: {train_data.shape}")
print(f"Testing data shape: {test_data.shape}")

# Save the train and test datasets
train_data.to_csv('processed/train_data.csv', index=False)
test_data.to_csv('processed/test_data.csv', index=False)

# Generate some visualizations
print("Generating visualizations...")

# 1. Total sales over time
plt.figure(figsize=(15, 6))
sales_by_date = sales_data.groupby('Date')['Sales_Quantity'].sum().reset_index()
plt.plot(sales_by_date['Date'], sales_by_date['Sales_Quantity'])
plt.title('Daily Total Sales')
plt.xlabel('Date')
plt.ylabel('Sales Quantity')
plt.grid(True)
plt.tight_layout()
plt.savefig('../images/daily_sales.png')

# 2. Sales by product category
plt.figure(figsize=(12, 6))
category_sales = sales_data.groupby('Category')['Sales_Quantity'].sum().sort_values(ascending=False).reset_index()
sns.barplot(x='Category', y='Sales_Quantity', data=category_sales)
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Sales Quantity')
plt.xticks(rotation=45)
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig('../images/category_sales.png')

# 3. Sales by region
plt.figure(figsize=(10, 6))
region_sales = sales_data.groupby('Region')['Sales_Quantity'].sum().sort_values(ascending=False).reset_index()
sns.barplot(x='Region', y='Sales_Quantity', data=region_sales)
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales Quantity')
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig('../images/region_sales.png')

# 4. Inventory vs Sales scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Sales_Quantity', y='Inventory_Level', data=sales_data.sample(1000, random_state=42), alpha=0.6)
plt.title('Sales Quantity vs Inventory Level')
plt.xlabel('Sales Quantity')
plt.ylabel('Inventory Level')
plt.grid(True)
plt.tight_layout()
plt.savefig('../images/sales_vs_inventory.png')

# 5. Weekly sales patterns
plt.figure(figsize=(10, 6))
day_of_week_sales = sales_data.groupby('DayOfWeek')['Sales_Quantity'].mean().reset_index()
day_of_week_sales['DayName'] = day_of_week_sales['DayOfWeek'].map({
    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
    4: 'Friday', 5: 'Saturday', 6: 'Sunday'
})
sns.barplot(x='DayName', y='Sales_Quantity', data=day_of_week_sales)
plt.title('Average Sales by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Sales Quantity')
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig('../images/day_of_week_sales.png')

print("Data preprocessing complete!")
print("Processed data saved to data/processed/")
print("Visualizations saved to images/")
