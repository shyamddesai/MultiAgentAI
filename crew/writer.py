import json

from crewai import Agent, Task
import os

from utils import get_openai_api_key
from dotenv import load_dotenv
from MultiAgentAI.crew.crew_tools import file_reader_tool
from crewai_tools import BaseTool


load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# -----------------------------------------------------------------------------

class MyCustomTool(BaseTool):
    name: str = "Saver Tool"
    description: str = "tool used to save output in a json file"

    def _run(self, argument: str) -> str:
        all_articles_output = "./reports/news_output1.json"
        with open(all_articles_output, 'w') as f:
             json.dump(argument, f, indent=2)
        return argument


save_into_json = MyCustomTool()

# ------------------------------------------------------------------------------
# Define the writer agent
writer_agent = Agent(
    role='Report Writer',
    goal='Generate a comprehensive report from provided content using read file tool',
    backstory="""You are a skilled Report Writer, known for your ability to transform raw content into polished, comprehensive reports.
                 You excel at identifying key points and presenting them in a clear, organized manner.""",
    verbose=True,
    allow_delegation=False

)

# Define the task for the writer agent
task = Task(
    description="""Read the content and information into a report.
                   The report should be structured in a paragraph form leaving no details behind. Save the report in a json file 
                   using save_into_json tool""",
    expected_output="A report saved in a separate json file",
    output_file="report.json",

    tools=[file_reader_tool, save_into_json],
    agent=writer_agent
)


