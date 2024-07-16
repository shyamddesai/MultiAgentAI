import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Process, Crew
from crewai_tools import FileReadTool
from utils import get_openai_api_key

# Load environment variables
load_dotenv()
openai_api_key = get_openai_api_key()
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the environment variables.")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# Define file paths
input_file_path = os.path.join(os.getcwd(), 'cleaned_exploration_news_report.json')
output_file_path = os.path.join(os.getcwd(), 'news_rank1.json')

# Initialize FileReadTool
read_file_tool = FileReadTool(file_path=input_file_path)

# Define the News Ranker agent
news_ranker = Agent(
    role="News Ranker",
    goal="Rank news articles based on relevancy to ADNOC Global Trading from JSON file including list of articles and their URL.",
    backstory=(
        "You're working on ranking these articles from a JSON file including list of articles and their URL. "
        "You base your ranking on ADNOC Global Trading and the traders there. They focus on the energy market and trade things like "
        "petroleum products, including diesel, gasoline, LPG, naphtha, biofuels, jet fuel, gas oil, and fuel oil. "
        "They deal in the worldwide market but are local to the Middle East and Gulf Region. They are also interested in things like WTI, Brent, and etc. "
        "ADNOC is an oil and gas company, one of the largest in the world. They are in the fields of drilling, energy, oil, and all similar areas. "
        "AGT's goal is 'to gather market and price intelligence to inform our decisions and optimize our business flows, to enable us to achieve greater efficiencies "
        "and performance for our clients, customers, and ADNOC Group Companies'. You acknowledge in your piece when your statements are analysis made by you."
    ),
    tools=[read_file_tool],
    verbose=True,
    memory=False
)

# Define the task for the News Ranker agent
news_rank_task = Task(
    description=(
        "Rank the articles in a list and give them a score from 1 to 10. "
        "10 being the highest relevancy to traders at ADNOC Global Trading. Be specific with "
        "reasoning for your ranking, and take into consideration "
        "what you know about ADNOC and the backstory. Be more meticulous with rankings. "
        "Read all the articles from JSON using the read_file tool."
    ),
    expected_output=(
        'Updated json file and fill in relevancy score and reasoning. Include '
        'the same Title, Link, Published, Categories, and Content from the read_file tool.'
    ),
    agent=news_ranker,
    output_file=output_file_path,
    verbose=True
)

# Initialize the Crew
crew = Crew(
    agents=[news_ranker],
    tasks=[news_rank_task],
    process=Process.sequential,
    verbose=True
)

# Execute the Crew
try:
    result = crew.kickoff()
    with open(output_file_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Results saved to {output_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
