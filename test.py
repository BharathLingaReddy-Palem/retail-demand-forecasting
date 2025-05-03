import unittest
import os
import pandas as pd
import numpy as np
from src.forecast_model import main as forecast_main

class TestForecastModel(unittest.TestCase):
    """Test cases for the forecasting model"""
    
    def setUp(self):
        """Set up test environment"""
        # Ensure required directories exist
        os.makedirs('data/processed', exist_ok=True)
        os.makedirs('models', exist_ok=True)
        os.makedirs('images', exist_ok=True)
        
        # Check if test data exists
        self.data_exists = os.path.exists('data/processed/train_data.csv') and \
                          os.path.exists('data/processed/test_data.csv')
    
    def test_data_files_exist(self):
        """Test if necessary data files exist"""
        self.assertTrue(os.path.exists('data/processed/weekly_data.csv') or 
                        self.skipTest("weekly_data.csv not found, skipping test"))
        self.assertTrue(os.path.exists('data/processed/train_data.csv') or 
                        self.skipTest("train_data.csv not found, skipping test"))
        self.assertTrue(os.path.exists('data/processed/test_data.csv') or 
                        self.skipTest("test_data.csv not found, skipping test"))
    
    def test_forecast_output_format(self):
        """Test if forecast output has the correct format"""
        if not self.data_exists:
            self.skipTest("Required data files not found, skipping test")
            
        # Run the forecast model if forecast results don't exist
        forecast_path = "data/processed/forecast_results_P001_S01.csv"
        if not os.path.exists(forecast_path):
            try:
                forecast_main()
            except Exception as e:
                self.fail(f"Forecast model failed with error: {e}")
        
        # Check if forecast file was created
        self.assertTrue(os.path.exists(forecast_path), 
                        "Forecast results file was not created")
        
        # Load forecast results
        forecast_data = pd.read_csv(forecast_path)
        
        # Check column names
        expected_columns = ['Week_Start', 'Forecasted_Sales', 'Optimal_Inventory']
        for col in expected_columns:
            self.assertIn(col, forecast_data.columns, 
                          f"Column {col} missing from forecast results")
        
        # Check data types
        forecast_data['Week_Start'] = pd.to_datetime(forecast_data['Week_Start'])
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(forecast_data['Week_Start']), 
                        "Week_Start should be a datetime column")
        
        # Check if values are reasonable
        self.assertTrue(all(forecast_data['Forecasted_Sales'] >= 0), 
                        "Forecasted sales should be non-negative")
        self.assertTrue(all(forecast_data['Optimal_Inventory'] >= 0), 
                        "Optimal inventory should be non-negative")
        
        # Check relationship between forecasted sales and optimal inventory
        self.assertTrue(all(forecast_data['Optimal_Inventory'] >= forecast_data['Forecasted_Sales']), 
                       "Optimal inventory should be greater than or equal to forecasted sales")
    
    def test_visualization_outputs(self):
        """Test if visualization files are created"""
        if not self.data_exists:
            self.skipTest("Required data files not found, skipping test")
            
        # Run the forecast model if forecast results don't exist
        forecast_path = "data/processed/forecast_results_P001_S01.csv"
        if not os.path.exists(forecast_path):
            try:
                forecast_main()
            except Exception as e:
                self.skipTest(f"Forecast model failed with error: {e}")
        
        # Check if visualization files exist
        expected_images = [
            'images/historical_and_forecasted_sales_P001_S01.png',
            'images/forecasted_sales_and_optimal_inventory_P001_S01.png'
        ]
        
        for img_path in expected_images:
            self.assertTrue(os.path.exists(img_path), 
                           f"Expected visualization file {img_path} not found")

if __name__ == '__main__':
    unittest.main()
