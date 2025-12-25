# Sales Data Analysis Dashboard

## Project Description
An interactive web-based dashboard built with Streamlit for analyzing sales data. This dashboard provides comprehensive insights into sales performance, customer behavior, and regional trends through interactive visualizations and filters.

## Objectives
- Analyze sales trends over time
- Identify top-performing products and regions
- Understand customer behavior patterns
- Provide interactive filtering capabilities
- Display key performance metrics in real-time

## Features
- **Interactive Filters**: Date range, product category, region, customer segment
- **Time Series Analysis**: Sales trends over time
- **Performance Analytics**: Top products and regions
- **Customer Insights**: Behavior patterns and segmentation
- **Geographic Analysis**: Sales heatmap by region and product
- **KPI Dashboard**: Key metrics and summary statistics

## Dataset Structure
The dashboard expects a CSV file with the following columns:
- `Date`: Transaction date (YYYY-MM-DD format)
- `Product`: Product name
- `Category`: Product category
- `Region`: Sales region
- `Sales`: Sales amount (numeric)
- `Quantity`: Number of items sold
- `Customer_ID`: Unique customer identifier
- `Customer_Segment`: Customer category (e.g., Consumer, Corporate, Home Office)
- `Discount`: Discount percentage applied
- `Profit`: Profit amount

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install streamlit pandas plotly numpy faker seaborn matplotlib
```

### Run the Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure
```
sales-dashboard/
├── README.md
├── dashboard.py          # Main Streamlit application
├── data_generator.py     # Sample data generation script
├── requirements.txt      # Python dependencies
└── data/
    └── sales_data.csv   # Generated sample dataset
```

## Future Enhancements
- Machine learning predictions for sales forecasting
- Advanced customer segmentation using clustering
- Export functionality for reports and charts
- Real-time data integration with databases
- Mobile-responsive design improvements
- Advanced filtering with multiple selections
- Drill-down capabilities for detailed analysis
- Integration with external APIs for market data