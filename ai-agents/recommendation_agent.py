# recommendation_agent.py

import os
from crewai import Agent, Task, Crew
from crewai_tools import BaseTool
from textwrap import dedent
import pandas as pd
import json

# Define the Recommendation Agent
recommendation_agent = Agent(
    role='Product Recommendation Specialist',
    goal='Recommend the top 2-3 products based on the customer’s needs.',
    backstory=dedent("""\
        You are an expert in the store's product catalog.
        Use the customer's preferences to recommend the best matching products.
        Provide clear and helpful explanations for your recommendations.
    """),
    allow_delegation=False,
    verbose=True
)

# Define the ProductSearchTool
class ProductSearchTool(BaseTool):
    name = "Product Search Tool"
    description = "Searches for products based on customer preferences."

    def __init__(self, product_data):
        self.product_data = product_data

    def _run(self, text):
        import json

        customer_needs = json.loads(text)
        filtered_products = self.product_data

        # Apply filters based on customer_needs
        if 'category' in customer_needs:
            filtered_products = filtered_products[filtered_products['category'].str.contains(customer_needs['category'], case=False, na=False)]
        if 'brand' in customer_needs:
            filtered_products = filtered_products[filtered_products['brand'].str.contains(customer_needs['brand'], case=False, na=False)]
        if 'price_range' in customer_needs:
            min_price, max_price = customer_needs['price_range']
            filtered_products = filtered_products[
                (filtered_products['price'] >= min_price) & (filtered_products['price'] <= max_price)
            ]
        if 'features' in customer_needs:
            features = customer_needs['features'].split(',')
            for feature in features:
                filtered_products = filtered_products[filtered_products['features'].str.contains(feature.strip(), case=False, na=False)]

        # Select top 2-3 products (you can sort by rating, popularity, etc.)
        recommended_products = filtered_products.head(3)

        # Convert the recommendations to a list of dictionaries
        products_list = recommended_products.to_dict('records')

        return json.dumps(products_list)

def recommend_products(customer_needs, product_data):
    # Instantiate the tool with the product data
    product_search_tool = ProductSearchTool(product_data)

    # Prepare inputs for the recommendation task
    inputs = {
        'user_needs': json.dumps(customer_needs)
    }

    # Define the Recommendation Task
    recommendation_task = Task(
        description=dedent("""\
            Based on the customer's needs provided, recommend the top 2-3 products.
            Customer needs: {user_needs}
            Provide a brief description of each product and explain why it matches the customer's needs.
        """),
        expected_output=dedent("""\
            A list of 2-3 recommended products with descriptions and reasons for recommendation.
        """),
        tools=[product_search_tool],
        agent=recommendation_agent
    )

    # Initialize the Crew
    crew = Crew(
        agents=[recommendation_agent],
        tasks=[],
        verbose=2,
        memory=True
    )

    # Run the Recommendation Task
    recommendation_result = crew.run_task(recommendation_task, inputs=inputs)
    return recommendation_result['response']  # Return the recommendations
