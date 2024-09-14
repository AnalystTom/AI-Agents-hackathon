import os
from dotenv import load_dotenv
from crewai import Crew
from need_analysis_agent import need_analysis_agent
from recommendation_agent import recommendation_agent
from need_analysis_task import need_analysis_task
from recommendation_task import recommendation_task

def main():
    # Load environment variables
    load_dotenv()

    # Initialize the Crew
    crew = Crew(
        agents=[need_analysis_agent, recommendation_agent],
        tasks=[need_analysis_task, recommendation_task],
        verbose=2,
        memory=False  # Disable memory to prevent potential issues
    )

    # Run the Crew
    inputs = {}
    result = crew.kickoff(inputs=inputs)

    # Display the final recommendations
    print("\nFinal Recommendations:")
    print(result)  # Remove ['response'] since result is a string

if __name__ == "__main__":
    main()
