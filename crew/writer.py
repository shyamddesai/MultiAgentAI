from crewai import Agent, Task
import os

from utils import get_openai_api_key
from dotenv import load_dotenv
from MultiAgentAI.crew.crew_tools import file_reader_tool



load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Define the writer agent
writer_agent = Agent(
    role='Report Writer',
    goal='Generate a comprehensive report from provided content of both the market analysis and sentiment analysis agents',
    backstory="""You are a skilled Report Writer, known for your ability to transform raw content into polished, comprehensive reports.
                 You excel at identifying key points and presenting them in a clear, organized manner.""",
    verbose=True,
    allow_delegation=False

)

# Define the task for the writer agent
task = Task(
    description="""Read the content and output of both agents and save their information into a report.
                   The report should be structured in a paragraph form leaving no details behind.""",
    expected_output="A report based of outputs of Market Analysis Agent and Sentiment Analysis Agent in a json file",
    output_file="report.json",
    tools=[file_reader_tool],
    agent=writer_agent
)


