"""
Sales Data Analysis Dashboard
Interactive Streamlit dashboard for sales data analysis and visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """
    Load and preprocess sales data
    
    Returns:
        pandas.DataFrame: Processed sales data
    """
    try:
        # Try to load existing data
        if os.path.exists('data/sales_data.csv'):
            df = pd.read_csv('data/sales_data.csv')
        else:
            st.error("Sales data not found. Please run data_generator.py first to create sample data.")
            st.stop()
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Add derived columns for analysis
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        df['Day_of_Week'] = df['Date'].dt.day_name()
        df['Month_Name'] = df['Date'].dt.month_name()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def create_sidebar_filters(df):
    """
    Create sidebar filters for data filtering
    
    Args:
        df (pandas.DataFrame): Sales data
    
    Returns:
        dict: Dictionary containing filter values
    """
    st.sidebar.markdown('<p class="sidebar-header">📊 Dashboard Filters</p>', unsafe_allow_html=True)
    
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Product category filter
    st.sidebar.subheader("🏷️ Product Category")
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Select category:", categories)
    
    # Region filter
    st.sidebar.subheader("🌍 Region")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Select region:", regions)
    
    # Customer segment filter
    st.sidebar.subheader("👥 Customer Segment")
    segments = ['All'] + sorted(df['Customer_Segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox("Select customer segment:", segments)
    
    # Product filter
    st.sidebar.subheader("📦 Product")
    products = ['All'] + sorted(df['Product'].unique().tolist())
    selected_product = st.sidebar.selectbox("Select product:", products)
    
    return {
        'date_range': date_range,
        'category': selected_category,
        'region': selected_region,
        'segment': selected_segment,
        'product': selected_product
    }

def filter_data(df, filters):
    """
    Apply filters to the dataset
    
    Args:
        df (pandas.DataFrame): Original dataset
        filters (dict): Filter parameters
    
    Returns:
        pandas.DataFrame: Filtered dataset
    """
    filtered_df = df.copy()
    
    # Apply date filter
    if len(filters['date_range']) == 2:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_date) & 
            (filtered_df['Date'].dt.date <= end_date)
        ]
    
    # Apply category filter
    if filters['category'] != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == filters['category']]
    
    # Apply region filter
    if filters['region'] != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == filters['region']]
    
    # Apply segment filter
    if filters['segment'] != 'All':
        filtered_df = filtered_df[filtered_df['Customer_Segment'] == filters['segment']]
    
    # Apply product filter
    if filters['product'] != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == filters['product']]
    
    return filtered_df

def display_kpi_metrics(df):
    """
    Display key performance indicators
    
    Args:
        df (pandas.DataFrame): Filtered sales data
    """
    # Calculate KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = len(df)
    avg_order_value = df['Sales'].mean()
    unique_customers = df['Customer_ID'].nunique()
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"${total_sales:,.2f}",
            delta=f"{total_orders} orders"
        )
    
    with col2:
        st.metric(
            label="📈 Total Profit",
            value=f"${total_profit:,.2f}",
            delta=f"{(total_profit/total_sales)*100:.1f}% margin" if total_sales > 0 else "0% margin"
        )
    
    with col3:
        st.metric(
            label="🛒 Average Order Value",
            value=f"${avg_order_value:.2f}",
            delta=f"{df['Quantity'].sum()} items sold"
        )
    
    with col4:
        st.metric(
            label="👥 Unique Customers",
            value=f"{unique_customers:,}",
            delta=f"{total_orders/unique_customers:.1f} orders/customer" if unique_customers > 0 else "0 orders/customer"
        )
    
    with col5:
        profit_margin = (total_profit/total_sales)*100 if total_sales > 0 else 0
        st.metric(
            label="📊 Profit Margin",
            value=f"{profit_margin:.1f}%",
            delta="Healthy" if profit_margin > 20 else "Needs attention"
        )

def create_time_series_chart(df):
    """
    Create time series chart of sales over time
    
    Args:
        df (pandas.DataFrame): Sales data
    
    Returns:
        plotly.graph_objects.Figure: Time series chart
    """
    # Aggregate sales by date
    daily_sales = df.groupby('Date').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Sales Revenue', 'Daily Profit'),
        vertical_spacing=0.1
    )
    
    # Add sales line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Sales'],
            mode='lines+markers',
            name='Sales Revenue',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Add profit line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Profit'],
            mode='lines+markers',
            name='Profit',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=4)
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title="Sales and Profit Trends Over Time",
        height=500,
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Sales ($)", row=1, col=1)
    fig.update_yaxes(title_text="Profit ($)", row=2, col=1)
    
    return fig

def create_top_products_chart(df, top_n=10):
    """
    Create bar chart of top products by sales
    
    Args:
        df (pandas.DataFrame): Sales data
        top_n (int): Number of top products to show
    
    Returns:
        plotly.graph_objects.Figure: Bar chart
    """
    # Aggregate by product
    product_sales = df.groupby('Product').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    # Get top products
    top_products = product_sales.nlargest(top_n, 'Sales')
    
    fig = px.bar(
        top_products,
        x='Sales',
        y='Product',
        orientation='h',
        title=f'Top {top_n} Products by Sales Revenue',
        labels={'Sales': 'Sales Revenue ($)', 'Product': 'Product'},
        color='Profit',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=400)
    
    return fig

def create_regional_performance_chart(df):
    """
    Create regional performance comparison
    
    Args:
        df (pandas.DataFrame): Sales data
    
    Returns:
        plotly.graph_objects.Figure: Regional chart
    """
    # Aggregate by region
    regional_data = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Customer_ID': 'nunique'
    }).reset_index()
    
    regional_data.columns = ['Region', 'Sales', 'Profit', 'Quantity', 'Customers']
    
    fig = px.bar(
        regional_data,
        x='Region',
        y='Sales',
        title='Sales Performance by Region',
        labels={'Sales': 'Sales Revenue ($)', 'Region': 'Region'},
        color='Profit',
        color_continuous_scale='Blues',
        text='Sales'
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig.update_layout(height=400)
    
    return fig

def create_customer_analysis_charts(df):
    """
    Create customer behavior analysis charts
    
    Args:
        df (pandas.DataFrame): Sales data
    
    Returns:
        tuple: Customer segment chart and repeat customer analysis
    """
    # Customer segment analysis
    segment_data = df.groupby('Customer_Segment').agg({
        'Sales': 'sum',
        'Customer_ID': 'nunique',
        'Quantity': 'sum'
    }).reset_index()
    
    segment_data['Avg_Order_Value'] = segment_data['Sales'] / segment_data['Customer_ID']
    
    # Pie chart for customer segments
    fig1 = px.pie(
        segment_data,
        values='Sales',
        names='Customer_Segment',
        title='Sales Distribution by Customer Segment',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Customer purchase frequency
    customer_orders = df.groupby('Customer_ID').size().reset_index(name='Order_Count')
    purchase_frequency = customer_orders.groupby('Order_Count').size().reset_index(name='Customer_Count')
    
    fig2 = px.bar(
        purchase_frequency.head(10),  # Show top 10 frequencies
        x='Order_Count',
        y='Customer_Count',
        title='Customer Purchase Frequency Distribution',
        labels={'Order_Count': 'Number of Orders', 'Customer_Count': 'Number of Customers'}
    )
    
    return fig1, fig2

def create_sales_heatmap(df):
    """
    Create heatmap of sales by region and product category
    
    Args:
        df (pandas.DataFrame): Sales data
    
    Returns:
        plotly.graph_objects.Figure: Heatmap
    """
    # Create pivot table
    heatmap_data = df.groupby(['Region', 'Category'])['Sales'].sum().reset_index()
    pivot_data = heatmap_data.pivot(index='Region', columns='Category', values='Sales').fillna(0)
    
    fig = px.imshow(
        pivot_data,
        title='Sales Heatmap: Region vs Product Category',
        labels=dict(x="Product Category", y="Region", color="Sales ($)"),
        aspect="auto",
        color_continuous_scale='RdYlBu_r'
    )
    
    fig.update_layout(height=400)
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Sales Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading sales data...'):
        df = load_data()
    
    # Sidebar filters
    filters = create_sidebar_filters(df)
    
    # Apply filters
    filtered_df = filter_data(df, filters)
    
    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("No data available for the selected filters. Please adjust your selection.")
        return
    
    # Display KPI metrics
    st.subheader("📈 Key Performance Indicators")
    display_kpi_metrics(filtered_df)
    
    st.divider()
    
    # Time series analysis
    st.subheader("📅 Sales Trends Over Time")
    time_series_fig = create_time_series_chart(filtered_df)
    st.plotly_chart(time_series_fig, use_container_width=True)
    
    # Two column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Products")
        top_products_fig = create_top_products_chart(filtered_df)
        st.plotly_chart(top_products_fig, use_container_width=True)
    
    with col2:
        st.subheader("🌍 Regional Performance")
        regional_fig = create_regional_performance_chart(filtered_df)
        st.plotly_chart(regional_fig, use_container_width=True)
    
    # Customer analysis
    st.subheader("👥 Customer Analysis")
    col3, col4 = st.columns(2)
    
    segment_fig, frequency_fig = create_customer_analysis_charts(filtered_df)
    
    with col3:
        st.plotly_chart(segment_fig, use_container_width=True)
    
    with col4:
        st.plotly_chart(frequency_fig, use_container_width=True)
    
    # Sales heatmap
    st.subheader("🔥 Sales Heatmap")
    heatmap_fig = create_sales_heatmap(filtered_df)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Data table (optional)
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            filtered_df.head(1000),  # Limit to first 1000 rows for performance
            use_container_width=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name=f"sales_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Sales Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>Data range: {} to {} | Total records: {:,}</p>
    </div>
    """.format(
        filtered_df['Date'].min().strftime('%Y-%m-%d'),
        filtered_df['Date'].max().strftime('%Y-%m-%d'),
        len(filtered_df)
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()