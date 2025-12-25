"""
Sales Data Generator
Generates realistic sample sales data for the dashboard demo
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Initialize Faker for generating realistic data
fake = Faker()
Faker.seed(42)  # For reproducible results
np.random.seed(42)

def generate_sales_data(num_records=5000):
    """
    Generate sample sales data with realistic patterns
    
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
    
    # Define regions with different performance characteristics
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Customer segments
    customer_segments = ['Consumer', 'Corporate', 'Home Office']
    
    # Generate date range (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()
    
    data = []
    
    # Generate customer pool
    customers = [f"CUST_{i:05d}" for i in range(1, 1001)]
    
    for _ in range(num_records):
        # Random date with seasonal patterns
        random_date = fake.date_between(start_date=start_date, end_date=end_date)
        
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
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        
        # Discount (0-30%, with most having no discount)
        discount = np.random.choice([0, 5, 10, 15, 20, 25, 30], 
                                  p=[0.6, 0.15, 0.1, 0.08, 0.04, 0.02, 0.01])
        
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
        month = random_date.month
        if month in [11, 12]:  # Holiday season boost
            sales_amount *= random.uniform(1.1, 1.3)
            profit *= random.uniform(1.1, 1.3)
        elif month in [6, 7, 8]:  # Summer boost for certain categories
            if category in ['Sports', 'Clothing']:
                sales_amount *= random.uniform(1.05, 1.15)
                profit *= random.uniform(1.05, 1.15)
        
        data.append({
            'Date': random_date,
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
    sales_df = generate_sales_data(5000)
    
    # Save to CSV
    output_path = 'data/sales_data.csv'
    sales_df.to_csv(output_path, index=False)
    
    print(f"Sample data generated successfully!")
    print(f"File saved: {output_path}")
    print(f"Records generated: {len(sales_df)}")
    print(f"Date range: {sales_df['Date'].min()} to {sales_df['Date'].max()}")
    print("\nDataset preview:")
    print(sales_df.head())
    print("\nDataset info:")
    print(sales_df.info())

if __name__ == "__main__":
    main()