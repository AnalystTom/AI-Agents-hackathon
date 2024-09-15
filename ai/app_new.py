import streamlit as st
import openai
import os
import mysql.connector
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
# Configure OpenAI API Key and Database
# -------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
}

# -------------------------
# Streamlit App Layout
# -------------------------
st.set_page_config(
    page_title="🛒 Product Recommendation Chatbot",
    page_icon=":shopping_cart:",
    layout="centered",
)

st.title("🛒 Product Recommendation Chatbot")
st.write("Hi! I'm here to help you find the perfect products. Let's get started!")

# -------------------------
# Initialize Session State
# -------------------------
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []  # To store the conversation history
if 'product_preferences' not in st.session_state:
    st.session_state['product_preferences'] = {}  # To store user preferences

# -------------------------
# Define System Prompt
# -------------------------
system_prompt = """
You are an E-commerce Product Recommendation Assistant for an online store. Your role is to engage users through interactive questions to understand their preferences and recommend relevant products from the store's database.

Ask questions one at a time, and adapt each new question based on the user’s previous responses.
Limit the number of questions to a maximum of 6 in total, focusing on narrowing down the user's specific needs.
After gathering sufficient information, ask the user for confirmation before making a recommendation.
If the user is ready, provide 2-3 product recommendations, each with a direct URL link to purchase.
Always ask: "Shall I recommend some products, or do you have any other preferences?"
If a user asks an unrelated or inappropriate query, politely respond while guiding the conversation back to product recommendations.
Example Flow:

Assistant: "Hi! Are you looking for any specific type of product today, like electronics, clothing, or something else?"
User: "I’m looking for a laptop."
Assistant: "Great! Do you have any preference for the brand or the operating system?"
User: "I prefer Windows laptops, no specific brand."
Assistant: "Noted. What’s your budget range for the laptop?"
User: "Around $800 to $1000."
Assistant: "Would you like features such as a touch screen or high-end graphics for gaming, or just basic performance for work?"
User: "I need it mainly for work, so performance is more important."
Assistant: "Thanks for the details! Shall I recommend a few options, or would you like to specify any other preferences?"
Once the user confirms, the assistant would respond with:

Assistant: "Based on your preferences, here are 2-3 laptops that match your needs:

Laptop A – High-performance laptop for work, 16GB RAM, Windows 11 ($950).
Laptop B – Ultra-slim, 8GB RAM, fast SSD storage, Windows 11 ($890).
Shall I assist you with anything else, or would you like more options?"
"""

# -------------------------
# Function to Query the Database
# -------------------------
def fetch_recommended_products(category, brand, price_range, features):
    conn = None
    cursor = None
    recommendations = []
    print(db_config)
    
    try:
        # Establish connection to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionaries
        
        query = """
        SELECT name, discount_price, image, link 
        FROM amazon_products 
        WHERE main_category = %s AND sub_category = %s AND discount_price <= %s AND sub_category LIKE %s
        LIMIT 3
        """
        print(category, brand, price_range, features)
        print(query)
        cursor.execute(query, (category, brand, price_range[1], f"%{features}%"))
        recommendations = cursor.fetchall()
        print("Recommendations from database: ",recommendations)
    
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return recommendations

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
    agent_response = "What type of product are you looking for from Amazon.com?"
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
        st.session_state['conversation'].append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        logger.info(f"User: {user_input}")
        
        agent_response = handle_conversation_logic(user_input)
        
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
# Conversation Logic
# -------------------------
def handle_conversation_logic(user_input):
    conversation = st.session_state['conversation']
    
    # Append user input to the conversation
    conversation.append({'role': 'user', 'content': user_input})
    
    # Use OpenAI to generate the next agent response based on user's input and conversation history
    agent_response = generate_agent_response(conversation)

    # If the conversation reaches the point of recommending products, use the database
    if "recommend" in agent_response.lower():
        product_type = st.session_state['product_preferences'].get("product_type", "electronics")
        budget = float(st.session_state['product_preferences'].get("budget", 1000))
        brand = st.session_state['product_preferences'].get("brand", "Any")
        features = st.session_state['product_preferences'].get("features", "")

        recommendations = fetch_recommended_products(product_type, brand, [0, budget], features)
        
        if recommendations:
            product_recommendations = "\n".join([
                f"**{prod['product_name']}** – ${prod['price']}, features: {prod['features']}\n[Buy Now]({prod['url']})"
                for prod in recommendations
            ])
            return f"Here are some products that match your preferences:\n{product_recommendations}"
        else:
            return "Sorry, I couldn't find any products that match your criteria."
    
    return agent_response

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
        st.session_state['product_preferences'] = {}
        st.session_state['user_input'] = ''
        logger.info("Conversation reset by user.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
