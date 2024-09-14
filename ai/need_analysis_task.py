from crewai import Task
from textwrap import dedent
from need_analysis_agent import need_analysis_agent

need_analysis_task = Task(
    description=dedent("""
        Engage with the customer to understand their product requirements.
        Ask one question at a time, wait for the customer's response, and proceed accordingly.
        Your goal is to gather all necessary information to recommend the best products.
        Ensure all interactions are appropriate and comply with OpenAI's usage policies.
    """),
    expected_output=dedent("""
        A detailed summary of the customer's needs and preferences in JSON format.
        Include keys like 'category', 'brand', 'price_range', 'features'.
    """),
    tools=[],
    agent=need_analysis_agent,
    human_input=True
)
