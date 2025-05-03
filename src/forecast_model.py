import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime, timedelta
import os
import pickle

# Set random seed for reproducibility
np.random.seed(42)

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Set2')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Create directories if they don't exist
os.makedirs('models', exist_ok=True)
os.makedirs('images', exist_ok=True)

def main():
    print("Loading processed data...")
    # Load the training and testing data
    train_data = pd.read_csv('data/processed/train_data.csv')
    test_data = pd.read_csv('data/processed/test_data.csv')

    # Convert date columns to datetime
    train_data['Week_Start'] = pd.to_datetime(train_data['Week_Start'])
    test_data['Week_Start'] = pd.to_datetime(test_data['Week_Start'])

    # Get unique product-store combinations
    product_store_combinations = train_data[['Product_ID', 'Store_ID']].drop_duplicates().values
    
    # For demonstration, select one product-store combination
    selected_idx = 0  # Can be changed to train different combinations
    product_id, store_id = product_store_combinations[selected_idx]
    
    print(f"Training model for Product: {product_id}, Store: {store_id}")
    
    # Filter data for the specific product and store
    train_product_store = train_data[(train_data['Product_ID'] == product_id) & 
                                    (train_data['Store_ID'] == store_id)].sort_values('Week_Start')
    test_product_store = test_data[(test_data['Product_ID'] == product_id) & 
                                   (test_data['Store_ID'] == store_id)].sort_values('Week_Start')
    
    # Select features
    features = ['Sales_Lag_1', 'Sales_Lag_2', 'Sales_Lag_3', 'Sales_Lag_4',
                'Sales_Rolling_2', 'Sales_Rolling_4', 'Sales_Rolling_8', 
                'Month', 'WeekOfYear', 'IsWeekend']
    
    # Add month and week features if not present
    if 'Month' not in train_product_store.columns:
        train_product_store['Month'] = train_product_store['Week_Start'].dt.month
        test_product_store['Month'] = test_product_store['Week_Start'].dt.month
    
    if 'WeekOfYear' not in train_product_store.columns:
        train_product_store['WeekOfYear'] = train_product_store['Week_Start'].dt.isocalendar().week
        test_product_store['WeekOfYear'] = test_product_store['Week_Start'].dt.isocalendar().week
    
    if 'IsWeekend' not in train_product_store.columns:
        train_product_store['IsWeekend'] = 0  # Assuming weekly data, set to 0
        test_product_store['IsWeekend'] = 0
    
    # Prepare features and target
    X_train = train_product_store[features]
    y_train = train_product_store['Sales_Quantity']
    
    X_test = test_product_store[features]
    y_test = test_product_store['Sales_Quantity']
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    # Make predictions
    print("Making predictions...")
    y_pred = rf_model.predict(X_test_scaled)
    
    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    
    # Plot actual vs predicted values
    plt.figure(figsize=(12, 6))
    plt.plot(test_product_store['Week_Start'], y_test, label='Actual Sales')
    plt.plot(test_product_store['Week_Start'], y_pred, label='Predicted Sales')
    plt.title(f'Actual vs Predicted Sales for {product_id} at {store_id}')
    plt.xlabel('Week')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'images/actual_vs_predicted_{product_id}_{store_id}.png')
    
    # Save the model
    with open(f'models/rf_model_{product_id}_{store_id}.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    
    # Forecast future demand
    print("Forecasting future demand...")
    
    # Function to forecast next n weeks
    def forecast_future_weeks(model, last_data, scaler, n_weeks=4):
        future_predictions = []
        current_features = last_data.copy()
        
        for i in range(n_weeks):
            # Scale the features
            current_features_scaled = scaler.transform([current_features])
            
            # Predict the next value
            next_sales = model.predict(current_features_scaled)[0]
            future_predictions.append(next_sales)
            
            # Update features for next prediction
            # Shift lag values
            current_features[0] = next_sales  # Sales_Lag_1 becomes the prediction
            current_features[1] = current_features[0]  # Sales_Lag_2 becomes previous Sales_Lag_1
            current_features[2] = current_features[1]  # Sales_Lag_3 becomes previous Sales_Lag_2
            current_features[3] = current_features[2]  # Sales_Lag_4 becomes previous Sales_Lag_3
            
            # Update rolling averages (simplified)
            current_features[4] = (current_features[0] + next_sales) / 2  # Sales_Rolling_2
            current_features[5] = (current_features[0] + current_features[1] + current_features[2] + next_sales) / 4  # Sales_Rolling_4
            # Keep Sales_Rolling_8 the same (simplified)
            
            # Update month and week (simplified)
            # For a real implementation, would need to properly increment date features
        
        return future_predictions
    
    # Get the last data point from test set
    last_data = X_test_scaled[-1].copy()
    
    # Forecast future weeks
    future_predictions = forecast_future_weeks(rf_model, last_data, scaler, n_weeks=4)
    
    # Create dates for the future predictions
    last_date = test_product_store['Week_Start'].iloc[-1]
    future_dates = [last_date + timedelta(weeks=i+1) for i in range(len(future_predictions))]
    
    # Calculate optimal inventory levels
    def calculate_optimal_inventory(forecasted_demand, safety_stock_factor=1.5, lead_time_days=3):
        # Convert lead time from days to weeks (assuming 7 days per week)
        lead_time_weeks = lead_time_days / 7
        
        # Calculate optimal inventory levels
        optimal_inventory = []
        for demand in forecasted_demand:
            # Base inventory = forecasted demand + safety stock
            base_inventory = demand * (1 + safety_stock_factor * lead_time_weeks)
            optimal_inventory.append(round(base_inventory))
        
        return optimal_inventory
    
    optimal_inventory = calculate_optimal_inventory(future_predictions)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'Week_Start': future_dates,
        'Forecasted_Sales': future_predictions,
        'Optimal_Inventory': optimal_inventory
    })
    
    print("Forecast Results:")
    print(forecast_df)
    
    # Save forecast results
    forecast_df.to_csv(f'data/processed/forecast_results_{product_id}_{store_id}.csv', index=False)
    
    # Plot historical and forecasted sales
    plt.figure(figsize=(15, 6))
    
    # Historical data
    historical_dates = list(train_product_store['Week_Start']) + list(test_product_store['Week_Start'])
    historical_sales = list(train_product_store['Sales_Quantity']) + list(test_product_store['Sales_Quantity'])
    plt.plot(historical_dates, historical_sales, label='Historical Sales', color='blue')
    
    # Forecasted data
    plt.plot(future_dates, future_predictions, label='Forecasted Sales', color='red', linestyle='--', marker='o')
    
    # Add vertical line to separate historical and forecasted data
    plt.axvline(x=last_date, color='gray', linestyle='--')
    plt.text(last_date, max(historical_sales), 'Forecast Start', ha='right', va='top')
    
    plt.title(f'Historical and Forecasted Sales for {product_id} at {store_id}')
    plt.xlabel('Date')
    plt.ylabel('Sales Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'images/historical_and_forecasted_sales_{product_id}_{store_id}.png')
    
    # Plot forecasted sales and optimal inventory levels
    plt.figure(figsize=(12, 6))
    
    # Bar chart for forecasted sales
    plt.bar(forecast_df['Week_Start'], forecast_df['Forecasted_Sales'], color='skyblue', label='Forecasted Sales')
    
    # Line chart for optimal inventory
    plt.plot(forecast_df['Week_Start'], forecast_df['Optimal_Inventory'], color='red', marker='o', label='Optimal Inventory')
    
    plt.title(f'Forecasted Sales and Optimal Inventory for {product_id} at {store_id}')
    plt.xlabel('Week')
    plt.ylabel('Quantity')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'images/forecasted_sales_and_optimal_inventory_{product_id}_{store_id}.png')
    
    print("Model training and forecasting complete!")
    print(f"Results saved to data/processed/forecast_results_{product_id}_{store_id}.csv")
    print(f"Visualizations saved to images/")

if __name__ == "__main__":
    main()
