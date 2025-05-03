import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
product_ids = [f'P{i:03d}' for i in range(1, 11)]  # 10 products
store_ids = [f'S{i:02d}' for i in range(1, 6)]     # 5 stores

# Create sample data
sales_data = []

for date in date_range:
    for product_id in product_ids:
        for store_id in store_ids:
            # Base sales with seasonal pattern
            base_sales = 50 + 30 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            # Add product-specific variation
            product_factor = int(product_id[1:]) / 10
            
            # Add store-specific variation
            store_factor = int(store_id[1:]) / 5
            
            # Add weekend effect
            weekend_factor = 1.2 if date.weekday() >= 5 else 1.0
            
            # Add holiday effect (simplified for demo)
            holiday_factor = 1.5 if (date.month == 12 and date.day >= 15) or (date.month == 11 and date.day >= 25) else 1.0
            
            # Add random noise
            noise = np.random.normal(0, 10)
            
            # Calculate sales quantity
            sales_qty = max(0, int(base_sales * product_factor * store_factor * weekend_factor * holiday_factor + noise))
            
            # Calculate inventory level (simple formula for demonstration)
            inventory_level = max(0, int(sales_qty * 1.5 + np.random.normal(0, 20)))
            
            # Add to dataset
            sales_data.append({
                'Date': date,
                'Product_ID': product_id,
                'Store_ID': store_id,
                'Sales_Quantity': sales_qty,
                'Inventory_Level': inventory_level
            })

# Convert to DataFrame
df_sales = pd.DataFrame(sales_data)

# Save raw data
os.makedirs('data/raw', exist_ok=True)
df_sales.to_csv('data/raw/sales_inventory_data.csv', index=False)
print(f"Generated {len(df_sales)} records of sample data.")
print(f"Data saved to data/raw/sales_inventory_data.csv")

# Create a smaller sample for quick testing
sample_df = df_sales.sample(n=10000, random_state=42)
sample_df.to_csv('data/raw/sample_data.csv', index=False)
print(f"Sample data with {len(sample_df)} records saved to data/raw/sample_data.csv")

# Generate product metadata
product_data = []
categories = ['Electronics', 'Clothing', 'Home Goods', 'Food', 'Toys']
for product_id in product_ids:
    product_num = int(product_id[1:])
    category = categories[product_num % len(categories)]
    price = 10 + (product_num * 5) + np.random.normal(0, 5)
    cost = price * 0.6
    product_data.append({
        'Product_ID': product_id,
        'Product_Name': f'Product {product_num}',
        'Category': category,
        'Price': round(max(5, price), 2),
        'Cost': round(max(3, cost), 2),
        'Weight_kg': round(0.5 + (product_num / 10), 2)
    })

# Convert to DataFrame and save
df_products = pd.DataFrame(product_data)
df_products.to_csv('data/raw/product_data.csv', index=False)
print(f"Product metadata saved to data/raw/product_data.csv")

# Generate store metadata
store_data = []
regions = ['North', 'South', 'East', 'West', 'Central']
for i, store_id in enumerate(store_ids):
    store_num = int(store_id[1:])
    region = regions[i % len(regions)]
    size = ['Small', 'Medium', 'Large'][store_num % 3]
    store_data.append({
        'Store_ID': store_id,
        'Store_Name': f'Store {store_num}',
        'Region': region,
        'Size': size,
        'Opening_Date': f"2020-{(store_num * 2) % 12 + 1:02d}-01"
    })

# Convert to DataFrame and save
df_stores = pd.DataFrame(store_data)
df_stores.to_csv('data/raw/store_data.csv', index=False)
print(f"Store metadata saved to data/raw/store_data.csv")

print("Sample data generation complete!")
