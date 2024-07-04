from crewai import Agent, Task
from dotenv import load_dotenv
from utils import get_openai_api_key
import os

load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key

news_analyst = Agent(
    role="Expert News Analyst",
    goal="Write insightful and factually accurate "
         "analytical piece from the data collected by the Researcher.",
    backstory="You're working on writing "
              "an analytical piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Senior News Researcher, who provides the relevant news "
              "and data about the topic: {topic}. "
              "You also provide accurate strategies and advice "
              "and back them up with information "
              "You acknowledge in your piece "
              "when your statements are analysis made by you.",
    verbose=True,
    memory=True,
)

analysis_task = Task(
    description=(
        "Analyze the gathered news articles from the News Researcher and identify key "
        "trends and insights in topic:{topic}. Summarize the information in a concise manner."
    ),
    expected_output='A summary report highlighting the key trends and insights from the analyzed news articles.',
    agent=news_analyst
)