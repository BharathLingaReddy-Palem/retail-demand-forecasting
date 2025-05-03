import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta

def generate_dashboard():
    """Generate a static dashboard with visualizations"""
    print("Generating static dashboard...")
    
    # Create output directory
    os.makedirs('reports/dashboard', exist_ok=True)
    
    # Load data
    try:
        weekly_data = pd.read_csv("data/processed/weekly_data.csv")
        weekly_data['Week_Start'] = pd.to_datetime(weekly_data['Week_Start'])
        
        forecast_path = "data/processed/forecast_results_P001_S01.csv"
        if os.path.exists(forecast_path):
            forecast_data = pd.read_csv(forecast_path)
            forecast_data['Week_Start'] = pd.to_datetime(forecast_data['Week_Start'])
        else:
            forecast_data = None
            
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Set plotting style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette('Set2')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    
    # 1. Weekly Sales Trend
    print("Generating weekly sales trend...")
    plt.figure(figsize=(12, 6))
    sales_by_week = weekly_data.groupby('Week_Start')['Sales_Quantity'].sum().reset_index()
    plt.plot(sales_by_week['Week_Start'], sales_by_week['Sales_Quantity'], marker='o')
    plt.title('Weekly Sales Trend', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Sales Quantity', fontsize=14)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/dashboard/weekly_sales_trend.png', dpi=300)
    plt.close()
    
    # 2. Top Products by Sales
    print("Generating top products chart...")
    plt.figure(figsize=(12, 6))
    product_sales = weekly_data.groupby('Product_ID')['Sales_Quantity'].sum().sort_values(ascending=False)
    sns.barplot(x=product_sales.index[:5], y=product_sales.values[:5])
    plt.title('Top 5 Products by Sales', fontsize=16)
    plt.xlabel('Product ID', fontsize=14)
    plt.ylabel('Total Sales', fontsize=14)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('reports/dashboard/top_products.png', dpi=300)
    plt.close()
    
    # 3. Top Stores by Sales
    print("Generating top stores chart...")
    plt.figure(figsize=(12, 6))
    store_sales = weekly_data.groupby('Store_ID')['Sales_Quantity'].sum().sort_values(ascending=False)
    sns.barplot(x=store_sales.index, y=store_sales.values)
    plt.title('Stores by Sales', fontsize=16)
    plt.xlabel('Store ID', fontsize=14)
    plt.ylabel('Total Sales', fontsize=14)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('reports/dashboard/store_sales.png', dpi=300)
    plt.close()
    
    # 4. Sales vs Inventory Scatter Plot
    print("Generating sales vs inventory scatter plot...")
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='Sales_Quantity', y='Inventory_Level', 
                   data=weekly_data.sample(500, random_state=42), alpha=0.6)
    plt.title('Sales Quantity vs Inventory Level', fontsize=16)
    plt.xlabel('Sales Quantity', fontsize=14)
    plt.ylabel('Inventory Level', fontsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('reports/dashboard/sales_vs_inventory.png', dpi=300)
    plt.close()
    
    # 5. Forecast Visualization (if available)
    if forecast_data is not None:
        print("Generating forecast visualization...")
        plt.figure(figsize=(12, 6))
        
        # Get historical data for P001 and S01
        historical_data = weekly_data[(weekly_data['Product_ID'] == 'P001') & 
                                     (weekly_data['Store_ID'] == 'S01')].sort_values('Week_Start')
        
        # Plot historical data (last 12 weeks)
        plt.plot(historical_data['Week_Start'].tail(12), 
                historical_data['Sales_Quantity'].tail(12), 
                marker='o', color='blue', label='Historical Sales')
        
        # Plot forecast
        plt.plot(forecast_data['Week_Start'], 
                forecast_data['Forecasted_Sales'], 
                marker='s', linestyle='--', color='red', label='Forecasted Sales')
        
        # Add vertical line to separate historical and forecasted data
        last_date = historical_data['Week_Start'].max()
        plt.axvline(x=last_date, color='gray', linestyle='--')
        
        plt.title('Sales Forecast for Product P001 at Store S01', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Sales Quantity', fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/dashboard/sales_forecast.png', dpi=300)
        plt.close()
        
        # 6. Optimal Inventory Visualization
        print("Generating optimal inventory visualization...")
        plt.figure(figsize=(12, 6))
        
        # Bar chart for forecasted sales
        x = range(len(forecast_data))
        plt.bar(x, forecast_data['Forecasted_Sales'], color='skyblue', label='Forecasted Sales')
        
        # Line chart for optimal inventory
        plt.plot(x, forecast_data['Optimal_Inventory'], color='red', marker='o', label='Optimal Inventory')
        
        plt.title('Forecasted Sales vs. Optimal Inventory', fontsize=16)
        plt.xlabel('Week', fontsize=14)
        plt.ylabel('Quantity', fontsize=14)
        plt.xticks(x, [d.strftime('%Y-%m-%d') for d in forecast_data['Week_Start']], rotation=45)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('reports/dashboard/optimal_inventory.png', dpi=300)
        plt.close()
    
    # Generate HTML dashboard
    print("Generating HTML dashboard...")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventory Optimization Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background-color: #f5f5f5;
                border-radius: 5px;
            }}
            h1 {{
                color: #1E88E5;
                margin-bottom: 10px;
            }}
            h2 {{
                color: #0D47A1;
                margin-top: 40px;
                border-bottom: 1px solid #ddd;
                padding-bottom: 10px;
            }}
            .visualization {{
                margin: 30px 0;
                text-align: center;
            }}
            .visualization img {{
                max-width: 100%;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .caption {{
                font-style: italic;
                text-align: center;
                margin-top: 10px;
                color: #666;
            }}
            .metrics-container {{
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
                flex-wrap: wrap;
            }}
            .metric-card {{
                background-color: #f5f5f5;
                border-radius: 5px;
                padding: 20px;
                text-align: center;
                width: 30%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #1565C0;
                margin-bottom: 10px;
            }}
            .metric-label {{
                font-size: 1rem;
                color: #424242;
            }}
            .footer {{
                margin-top: 50px;
                text-align: center;
                color: #666;
                font-size: 0.9rem;
                border-top: 1px solid #ddd;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Inventory Optimization Dashboard</h1>
            <p>AI-Based Inventory Optimization for Retail Chains</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>

        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-value">{weekly_data['Sales_Quantity'].sum():,.0f}</div>
                <div class="metric-label">Total Sales</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{weekly_data['Inventory_Level'].mean():,.1f}</div>
                <div class="metric-label">Average Inventory</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{weekly_data['Product_ID'].nunique()}</div>
                <div class="metric-label">Number of Products</div>
            </div>
        </div>

        <h2>Sales and Inventory Trends</h2>
        
        <div class="visualization">
            <img src="weekly_sales_trend.png" alt="Weekly Sales Trend">
            <p class="caption">Weekly sales showing seasonal patterns and overall trends</p>
        </div>

        <div class="visualization">
            <img src="sales_vs_inventory.png" alt="Sales vs Inventory">
            <p class="caption">Relationship between sales quantity and inventory level</p>
        </div>

        <h2>Product and Store Analysis</h2>
        
        <div class="visualization">
            <img src="top_products.png" alt="Top Products by Sales">
            <p class="caption">Top 5 products by total sales quantity</p>
        </div>

        <div class="visualization">
            <img src="store_sales.png" alt="Store Sales">
            <p class="caption">Sales performance by store</p>
        </div>
    """
    
    # Add forecast section if available
    if forecast_data is not None:
        html_content += """
        <h2>Demand Forecasting</h2>
        
        <div class="visualization">
            <img src="sales_forecast.png" alt="Sales Forecast">
            <p class="caption">Historical and forecasted sales for Product P001 at Store S01</p>
        </div>

        <div class="visualization">
            <img src="optimal_inventory.png" alt="Optimal Inventory">
            <p class="caption">Forecasted sales and recommended optimal inventory levels</p>
        </div>
        """
    
    # Add footer
    html_content += """
        <div class="footer">
            <p>Inventory Optimization Dashboard | Powered by Machine Learning</p>
            <p>© 2025 Retail Analytics</p>
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    with open('reports/dashboard/index.html', 'w') as f:
        f.write(html_content)
    
    print("Static dashboard generated successfully!")
    print("Dashboard saved to reports/dashboard/")
    print("Open reports/dashboard/index.html in your web browser to view the dashboard")

if __name__ == "__main__":
    generate_dashboard()
