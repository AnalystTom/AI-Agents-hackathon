import os
import pandas as pd
import need_analysis_agent
import recommendation_agent

# Setup environment variables
os.environ["OPENAI_API_KEY"] = 'your-openai-api-key'  # Replace with your API key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

def main():
    # Load product data from CSV
    product_data = pd.read_csv('products.csv')  # Ensure 'products.csv' is in your working directory

    # Collect user needs using the Need Analysis Agent
    customer_needs = need_analysis_agent.collect_user_needs()

    # Generate product recommendations using the Recommendation Agent
    recommendations = recommendation_agent.recommend_products(customer_needs, product_data)

    # Display the recommendations
    print("\nRecommendations:")
    print(recommendations)

if __name__ == "__main__":
    main()
