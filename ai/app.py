import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# -------------------------
# Configure Logging
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()  # Load variables from .env

# -------------------------
# Configure OpenAI API Key
# -------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------
# Streamlit App Layout
# -------------------------
st.set_page_config(
    page_title="🛒 Amazon.com Product Recommendation Chatbot",
    page_icon=":shopping_cart:",
    layout="centered",
)

st.title("🛒 Amazon.com Product Recommendation Chatbot")
st.write("Hi! I'm here to help you find the perfect products from Amazon.com. Let's get started!")

# -------------------------
# Initialize Session State
# -------------------------
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []  # To store the conversation history

# -------------------------
# Define System Prompt
# -------------------------
system_prompt = """
You are a helpful E-commerce Product Recommendation Assistant for Amazon.com. Your job is to assist customers by recommending products from the Amazon.com product catalogue. You will ask at least 6 interactive questions one by one to understand their needs and provide the top 2-3 product recommendations with direct URL links to buy. If a customer asks something relevant to the website or the company, you will provide the customer care email. For unrelated questions, you will politely decline.

Key Instructions:
- Start by asking what type of product the user is looking for from Amazon.com (e.g., electronics, books, home appliances).
- Ask at least 6 interactive questions one by one without numbering them and make them explicit to the customer.
  - Budget.
  - Specific preferences (e.g., brand, features, size).
  - Usage frequency or purpose.
  - Any specific requirements (e.g., color, material).
  - Delivery timeframe.
  - Any other preferences before recommending products.
- Respond to relevant questions about the website or company by providing the email:
  "Please contact our customer care at service@amazon.com for assistance."
- For unrelated questions (e.g., general topics outside of Amazon.com products), respond with:
  "Sorry, I can respond only to product-related queries from our company."
- Provide the top 2-3 product recommendations with key features, price, and a direct "Add to Cart" link for each product.
- Offer basic usage instructions if applicable.

Example Interaction:
User Input: "I need a good face cream for aging skin."

Your Output:
"What is your budget for the face cream?"
User Input: "Around $50."

Your Output:
"Do you have any specific concerns like wrinkles or fine lines?"
User Input: "Yes, wrinkles."

Your Output:
"Would you prefer natural ingredients?"
User Input: "Yes, please."

Your Output:
"Do you have a brand preference?"
User Input: "No preference."

Your Output:
"How often do you plan to use this cream?"
User Input: "Twice a day."

Your Output:
"Any other preferences I should know?"
User Input: "No, that's all."

Your Output:
"Here are 2 anti-aging creams with natural ingredients under $50:

1. **Anti-Aging Cream A** – $48, helps reduce wrinkles and hydrates deeply.
   [Add to Cart](https://www.amazon.com/product/anti-aging-cream-a)

2. **Anti-Aging Cream B** – $45, natural formula for wrinkle reduction and skin elasticity.
   [Add to Cart](https://www.amazon.com/product/anti-aging-cream-b)"

Provide usage instructions:
"Apply twice daily on clean skin for best results."

User Input: "Can you help me with shipping information?"

Your Output:
"Please contact our customer care at service@amazon.com for assistance."

User Input: "Who won the last soccer world cup?"

Your Output:
"Sorry, I can respond only to product-related queries from our company."
"""

# -------------------------
# Function to Generate Agent Response
# -------------------------
def generate_agent_response(conversation):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation,
            max_tokens=800,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # Corrected access method using attribute access
        agent_message = response.choices[0].message['content'].strip()
        return agent_message
    except openai.error.RateLimitError:
        logger.error("OpenAI API Rate Limit Exceeded")
        return "**Agent:** Sorry, I'm experiencing high traffic. Please try again later."
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        return f"**Agent:** Sorry, I encountered an error: {e}"

# -------------------------
# Function to Initialize Conversation
# -------------------------
def initialize_conversation():
    st.session_state['conversation'].append({
        'role': 'system',
        'content': system_prompt
    })
    # Generate the first agent prompt based on the system prompt
    agent_response = generate_agent_response(st.session_state['conversation'])
    st.session_state['conversation'].append({
        'role': 'assistant',
        'content': agent_response,
        'timestamp': datetime.now().isoformat()
    })
    logger.info("Initialized conversation with system prompt and first agent response.")

# -------------------------
# Display Conversation
# -------------------------
def display_conversation():
    for message in st.session_state['conversation']:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
            logger.info(f"Displayed User Message: {message['content']}")
        elif message['role'] == 'assistant':
            st.markdown(f"**Agent:** {message['content']}")
            logger.info(f"Displayed Agent Message: {message['content']}")
        # Skip messages with role 'system'

# -------------------------
# Handle User Input and Generate Response
# -------------------------
def handle_input():
    user_input = st.session_state['user_input'].strip()
    if user_input:
        # Append user message to conversation
        st.session_state['conversation'].append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        logger.info(f"User: {user_input}")
        
        # Show spinner while generating response
        with st.spinner('Generating recommendations...'):
            agent_response = generate_agent_response(st.session_state['conversation'])
        
        logger.info(f"Agent: {agent_response}")
        
        # Append agent response to conversation
        st.session_state['conversation'].append({
            'role': 'assistant',
            'content': agent_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Clear user input
        st.session_state['user_input'] = ''
        
        # Rerun to display the new messages
        st.experimental_rerun()

# -------------------------
# Main App Logic
# -------------------------
def main():
    # Initialize conversation with system prompt if it's the first run
    if len(st.session_state['conversation']) == 0:
        initialize_conversation()
    
    # Display the conversation
    st.markdown("### Conversation:")
    display_conversation()
    
    # Input form for user message
    st.text_input("You:", key='user_input', on_change=handle_input)
    
    # Reset Conversation Button
    if st.button("Reset Conversation"):
        st.session_state['conversation'] = []
        st.session_state['user_input'] = ''
        logger.info("Conversation reset by user.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
