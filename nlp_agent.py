import openai
import json

def process_user_input(input_text):
    prompt = f"""
    Extract the user's intent and relevant product details from the following input. Provide the output in JSON format with keys 'intent', 'product_category', 'features', 'price_range', and 'other_constraints'.

    User Input: "{input_text}"
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        n=1,
        stop=None,
    )
    response_text = response.choices[0].text.strip()
    try:
        processed_data = json.loads(response_text)
    except json.JSONDecodeError:
        # Handle parsing error
        processed_data = None
    return processed_data
