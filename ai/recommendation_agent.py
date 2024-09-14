from crewai import Agent
from textwrap import dedent
import json

class RecommendationAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Product Recommendation Specialist',
            goal='Recommend the top 2-3 products based on the customer’s needs.',
            backstory=dedent("""
                You are an expert in the store's product catalog.
                Use the customer's preferences to recommend the best matching products.
                Provide clear and helpful explanations for your recommendations.
            """),
            allow_delegation=False,
            verbose=True
        )

    def execute_task(self, task, context=None, tools=None, **kwargs):
        # Check if context is a string
        if isinstance(context, str):
            # context is the JSON string of customer needs
            customer_needs = json.loads(context)
        elif isinstance(context, dict) and 'previous_task_output' in context:
            # context is a dictionary with previous_task_output
            customer_needs = json.loads(context['previous_task_output'])
        else:
            raise ValueError("Invalid context format received by RecommendationAgent.")

        # Use the product search tool to find products
        product_search_tool = tools[0]  # Assuming only one tool is passed
        recommended_products_json = product_search_tool._run(json.dumps(customer_needs))
        recommended_products = json.loads(recommended_products_json)

        # Generate recommendations
        recommendations = []
        for product in recommended_products:
            recommendation = f"Product Name: {product.get('product_name', 'N/A')}\n"
            recommendation += f"Description: {product.get('Product Description', 'N/A')}\n"
            recommendation += f"Price: ${product.get('price', 'N/A')}\n"
            recommendation += f"Reason: Matches your preferences.\n"
            recommendations.append(recommendation)

        # Return the recommendations as a single string
        return '\n\n'.join(recommendations)

recommendation_agent = RecommendationAgent()
