# Inventory Optimization for Retail Using Predictive Analytics

## Sales and Inventory Forecasting System

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2.2-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-red.svg)

An AI-powered sales and inventory forecasting system that helps retailers optimize inventory levels, reduce costs, and improve customer satisfaction through data-driven predictions.

## 📊 Demo



*The interactive dashboard provides real-time insights and forecasts for business users*

## 🔍 Overview

This system uses historical sales data to train a Random Forest model that predicts future demand for each product-store combination. Based on these predictions, it calculates optimal inventory levels that minimize costs while avoiding stockouts.

## ✨ Key Features

- **Data Preprocessing**: Clean and transform raw sales data into features suitable for forecasting
- **Advanced Forecasting**: Time series prediction using Random Forest algorithms
- **Inventory Optimization**: Calculate optimal stock levels based on forecasts
- **Interactive Dashboard**: Visualize trends, forecasts, and insights
- **Comprehensive Reporting**: Generate detailed HTML reports with visualizations



## 🗂️ Project Structure

```
/Inventory-Optimization-Project/
│
├── 📁 data/                  ← raw & processed data
├── 📁 notebooks/            ← Jupyter notebooks
├── 📁 images/               ← result charts for PPT
├── 📁 ppt/                  ← final .pptx
├── 📄 README.md             ← full project summary
└── 📄 requirements.txt      ← Python packages used
```

## Components
1. **Data Collection**: Use historical inventory and sales data
2. **Data Preprocessing**: Clean and organize time series data (e.g., product-wise monthly/weekly sales)
3. **Feature Engineering**: Include time (month, day), category, holidays, and promotional events
4. **Modeling**: Use LSTM or ARIMA for time series prediction
5. **Deployment**: Build a dashboard (e.g., in Streamlit) for real-time inventory insights

## Technologies Used
- Python (Pandas, Scikit-learn, Keras/TensorFlow)
- Jupyter Notebook


## Libraries
- pandas, numpy, matplotlib, seaborn
- scikit-learn
- statsmodels

## Algorithm
- LSTM (Long Short-Term Memory) for sequence-based demand forecasting

## Input Data
- Product ID
- Date
- Sales Quantity
- Store ID
- Inventory on hand

## Training Process
- Train LSTM on weekly sales data
- Normalize and structure data into sequences
- Use rolling-window technique for prediction

## Prediction Process
- Forecast next week's demand
- Provide restocking recommendation using predicted demand

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Run the Jupyter notebooks in the notebooks/ directory to see the data analysis and model development
2. Use the Streamlit dashboard for interactive forecasting and inventory optimization

## Contributors
- Bharath Linga Reddy


