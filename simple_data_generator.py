"""
Simple Sales Data Generator
Creates sample sales data without external dependencies
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

def generate_simple_sales_data(num_records=2000):
    """
    Generate sample sales data using only built-in libraries
    
    Args:
        num_records (int): Number of records to generate
    
    Returns:
        pandas.DataFrame: Generated sales dataset
    """
    
    # Define product categories and products
    categories = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
        'Home & Garden': ['Sofa', 'Table', 'Chair', 'Lamp', 'Plant'],
        'Books': ['Fiction Novel', 'Textbook', 'Cookbook', 'Biography', 'Self-Help'],
        'Sports': ['Basketball', 'Tennis Racket', 'Running Shoes', 'Yoga Mat', 'Bicycle']
    }
    
    # Define regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Customer segments
    customer_segments = ['Consumer', 'Corporate', 'Home Office']
    
    # Generate date range (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    
    data = []
    
    # Generate customer pool
    customers = [f"CUST_{i:05d}" for i in range(1, 501)]
    
    for i in range(num_records):
        # Random date
        random_days = random.randint(0, 729)
        record_date = start_date + timedelta(days=random_days)
        
        # Select category and product
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        # Region selection
        region = random.choice(regions)
        
        # Customer segment
        segment = random.choice(customer_segments)
        
        # Customer ID (some customers make multiple purchases)
        customer_id = random.choice(customers)
        
        # Generate sales amount based on product category
        base_prices = {
            'Electronics': (200, 2000),
            'Clothing': (20, 200),
            'Home & Garden': (50, 1000),
            'Books': (10, 50),
            'Sports': (30, 500)
        }
        
        min_price, max_price = base_prices[category]
        base_price = random.uniform(min_price, max_price)
        
        # Quantity (most orders are 1-3 items)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
        
        # Discount (0-30%, with most having no discount)
        discount = random.choices([0, 5, 10, 15, 20, 25, 30], 
                                weights=[60, 15, 10, 8, 4, 2, 1])[0]
        
        # Calculate sales amount
        sales_amount = base_price * quantity * (1 - discount/100)
        
        # Profit margin varies by category
        profit_margins = {
            'Electronics': 0.15,
            'Clothing': 0.40,
            'Home & Garden': 0.25,
            'Books': 0.20,
            'Sports': 0.30
        }
        
        profit = sales_amount * profit_margins[category] * random.uniform(0.8, 1.2)
        
        # Add seasonal effects
        month = record_date.month
        if month in [11, 12]:  # Holiday season boost
            sales_amount *= random.uniform(1.1, 1.3)
            profit *= random.uniform(1.1, 1.3)
        elif month in [6, 7, 8]:  # Summer boost for certain categories
            if category in ['Sports', 'Clothing']:
                sales_amount *= random.uniform(1.05, 1.15)
                profit *= random.uniform(1.05, 1.15)
        
        data.append({
            'Date': record_date.strftime('%Y-%m-%d'),
            'Product': product,
            'Category': category,
            'Region': region,
            'Sales': round(sales_amount, 2),
            'Quantity': quantity,
            'Customer_ID': customer_id,
            'Customer_Segment': segment,
            'Discount': discount,
            'Profit': round(profit, 2)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df

def main():
    """Generate and save sample sales data"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("Generating sample sales data...")
    
    # Generate data
    sales_df = generate_simple_sales_data(2000)
    
    # Save to CSV
    output_path = 'data/sales_data.csv'
    sales_df.to_csv(output_path, index=False)
    
    print(f"Sample data generated successfully!")
    print(f"File saved: {output_path}")
    print(f"Records generated: {len(sales_df)}")
    print(f"Date range: {sales_df['Date'].min()} to {sales_df['Date'].max()}")
    print("\nDataset preview:")
    print(sales_df.head())

if __name__ == "__main__":
    main()