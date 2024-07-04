from crewai import Agent, Task
from dotenv import load_dotenv
from utils import get_openai_api_key
import os

load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key

writer = Agent(
    role="Editor",
    goal="Edit the analytical piece done by the Expert News Analyst "
         "into a professional and well structured news summary.",
    backstory="You are an experienced and well-trained editor who receives news analysis "
              "from the Expert News Analyst. "
              "Your goal is to review the analysis ensuring that the "
              "final report is clear and engaging.",
    verbose=True,
    memory=True
)

editing_task = Task(
    description=(
        "Compile the analyzed information into a well-structured report. "
        "Ensure that the report is clear, engaging, and free of errors."
    ),
    expected_output='A final report in markdown format that is well-structured and engaging.',
    agent=writer
)