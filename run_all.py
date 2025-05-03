#!/usr/bin/env python
"""
Run all components of the Sales & Inventory Forecasting System in sequence.
This script will:
1. Generate sample data
2. Preprocess the data
3. Train the forecasting model
4. Generate the HTML report
"""

import os
import subprocess
import time
import sys

def run_script(script_name, description):
    """Run a Python script and display its output"""
    print(f"\n{'=' * 80}")
    print(f"Running: {description}")
    print(f"{'=' * 80}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, f"src/{script_name}"],
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors:\n{result.stderr}")
        
        elapsed = time.time() - start_time
        print(f"\nCompleted in {elapsed:.2f} seconds")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stderr)
        return False

def main():
    """Run all components of the system"""
    # Ensure we're in the project root directory
    if not os.path.exists('src'):
        print("Error: This script must be run from the project root directory")
        return
    
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Run each component
    steps = [
        ('generate_sample_data.py', 'Generating sample data'),
        ('preprocess_data.py', 'Preprocessing data'),
        ('forecast_model.py', 'Training forecasting model'),
        ('generate_html_report.py', 'Generating HTML report')
    ]
    
    for script, description in steps:
        success = run_script(script, description)
        if not success:
            print(f"\nError in {script}. Stopping execution.")
            return
    
    # Final message
    print("\n" + "=" * 80)
    print("All components executed successfully!")
    print("=" * 80)
    print("\nTo run the interactive dashboard, use:")
    print("    streamlit run src/dashboard.py")
    print("\nTo view the generated report, open:")
    print("    reports/Sales_Inventory_Optimization_Report.html")

if __name__ == "__main__":
    main()
