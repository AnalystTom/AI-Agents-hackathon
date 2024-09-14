# recommendation_task.py

from crewai import Task
from textwrap import dedent
from recommendation_agent import recommendation_agent
from product_search_tool import ProductSearchTool
import pandas as pd

# Load product data
product_data = pd.read_csv('ai-agents/products.csv')

# Preprocess the data to match expected column names
product_data.rename(columns={
    'Product Name': 'product_name',
    'Product Category': 'category',
    'Brand': 'brand',
    'Price': 'price',
    'Specifications': 'features'
}, inplace=True)

# Ensure price is numeric
product_data['price'] = pd.to_numeric(product_data['price'], errors='coerce')

# Handle missing values
product_data['features'] = product_data['features'].fillna('')
product_data['brand'] = product_data['brand'].fillna('')
product_data['category'] = product_data['category'].fillna('')

# Initialize the tool
product_search_tool = ProductSearchTool(product_data=product_data)

recommendation_task = Task(
    description=dedent("""
        Based on the customer's needs collected, recommend the top 2-3 products.
        Provide a brief description of each product and explain why it matches the customer's needs.
        Use the Product Search Tool to find suitable products.
    """),
    expected_output=dedent("""
        A list of 2-3 recommended products with descriptions and reasons for recommendation.
    """),
    tools=[product_search_tool],
    agent=recommendation_agent
)
