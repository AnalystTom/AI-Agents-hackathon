from pydantic import Field
from crewai import Agent
from textwrap import dedent
import json
import re
from typing import Dict

class NeedAnalysisAgent(Agent):
    customer_needs: Dict = Field(default_factory=dict)

    def __init__(self):
        super().__init__(
            role='Customer Need Analysis Specialist',
            goal='Understand the customer’s product needs by asking relevant questions one by one.',
            backstory=dedent("""
                You are a friendly and patient assistant at an e-commerce store.
                Your task is to help customers find the perfect product by asking them questions.
                Ask one question at a time and wait for the customer's response before proceeding.
                Focus on gathering information that will help in filtering products, such as category, brand, price range, and features.
            """),
            allow_delegation=False,
            verbose=True
        )

    def execute_task(self, task, context=None, tools=None, **kwargs):
        print("Agent: Hello! I'm here to help you find the perfect product. Could you tell me what you're looking for?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['no', "that's all", 'nothing else', 'no more', 'done']:
                print("Agent: Thank you for the information!")
                break
            else:
                if 'category' not in self.customer_needs:
                    self.customer_needs['category'] = user_input
                    print("Agent: Do you have a preferred brand?")
                elif 'brand' not in self.customer_needs:
                    self.customer_needs['brand'] = user_input
                    print("Agent: What is your budget or price range?")
                elif 'price_range' not in self.customer_needs:
                    prices = re.findall(r'\d+', user_input.replace(',', ''))
                    if len(prices) >= 2:
                        min_price, max_price = map(float, prices[:2])
                    elif len(prices) == 1:
                        min_price = 0
                        max_price = float(prices[0])
                    else:
                        min_price = 0
                        max_price = 1000000  # Default max price
                    self.customer_needs['price_range'] = [min_price, max_price]
                    print("Agent: Are there specific features you're looking for?")
                elif 'features' not in self.customer_needs:
                    self.customer_needs['features'] = user_input
                    print("Agent: Any other preferences? If not, please type 'done'.")
                else:
                    print("Agent: Any other preferences? If not, please type 'done'.")
        # Return the customer needs as a JSON string
        return json.dumps(self.customer_needs)

need_analysis_agent = NeedAnalysisAgent()
