# need_analysis_agent.py

import os
from crewai import Agent
from textwrap import dedent
import json

# Define the Need Analysis Agent
need_analysis_agent = Agent(
    role='Customer Need Analysis Specialist',
    goal='Understand the customer’s product needs by asking relevant questions one by one.',
    backstory=dedent("""\
        You are a friendly and patient assistant at an e-commerce store.
        Your task is to help customers find the perfect product by asking them questions.
        Ask one question at a time and wait for the customer's response before proceeding.
        Focus on gathering information that will help in filtering products, such as category, brand, price range, and features.
    """),
    allow_delegation=False,
    verbose=True
)

def collect_user_needs():
    print("Agent: Hello! I'm here to help you find the perfect product. Could you tell me what you're looking for?")

    user_needs = {}
    questions_asked = []

    attribute_mapping = {
        'What category of products are you interested in?': 'category',
        'Do you have a preferred brand?': 'brand',
        'What is your budget or price range?': 'price_range',
        'Are there specific features you\'re looking for?': 'features'
    }

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['no', 'that\'s all', 'nothing else', 'no more']:
            print("Agent: Thank you for the information!")
            break
        else:
            # Store user's response
            if questions_asked:
                last_question = questions_asked[-1]
                user_needs[last_question] = user_input
            else:
                user_needs['initial_request'] = user_input

            # Agent determines the next question
            next_question = need_analysis_agent.act(
                f"The customer said: '{user_input}'. Based on this, what is the next most important question to ask to understand their needs better? Focus on attributes like category, brand, price range, features, etc.",
                memory=True
            )
            question_text = next_question['response']
            print(f"Agent: {question_text}")
            questions_asked.append(question_text)

    # Map user responses to product attributes
    customer_needs = {}
    for question, response in user_needs.items():
        attribute = attribute_mapping.get(question)
        if attribute:
            if attribute == 'price_range':
                # Process price range (e.g., "between $100 and $200")
                import re
                prices = re.findall(r'\d+', response.replace(',', ''))
                if len(prices) >= 2:
                    min_price, max_price = map(float, prices[:2])
                    customer_needs[attribute] = (min_price, max_price)
            else:
                customer_needs[attribute] = response

    return customer_needs  # Return the collected customer needs
