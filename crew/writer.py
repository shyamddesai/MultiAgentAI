import json

from crewai import Agent, Task
import os

from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from utils import get_openai_api_key
from dotenv import load_dotenv
from MultiAgentAI.crew.crew_tools import file_reader_tool
from crewai_tools import BaseTool

# -----------------------------------------------------------------------------
# Define file paths
input_file_path = '/MultiAgentAI/Files I do not think we need/news_report_analysis_parallel.md'
output_file_path = 'C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/reports/news_output1.json'

# Load environment variables
load_dotenv()
openai_api_key = get_openai_api_key()
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the environment variables.")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


# Initialize FileReadTool
file_reader_tool = FileReadTool(file_path=input_file_path)

class SaverTool(BaseTool):
    name: str = "Saver Tool"
    description: str = "Tool used to save output in a JSON file"

    def _run(self, argument: str) -> str:
        with open(output_file_path, 'w') as f:
            json.dump(argument, f, indent=2)
        return argument

# Initialize SaverTool
save_into_json = SaverTool()

output_file_path_report = os.path.join(os.getcwd(), '../reports/final_news_report.json')

# Define the writer agent
writer_agent = Agent(
    role='Report Writer',
    goal='Generate a comprehensive report from provided content using the read file tool',
    backstory="""You are a skilled Report Writer, known for your ability to transform raw content into polished, comprehensive reports.
                 You excel at identifying key points and presenting them in a clear, organized manner.""",
    verbose=True,
    allow_delegation=False
)

# Define the task for the writer agent
writer_task = Task(
    description="""Read the content and transform the information into a report.
                   The report should be structured in paragraph form, leaving no details behind. Save the report in a JSON file 
                   using save_into_json tool.""",
    expected_output="A report that is professionally written in a proper format",
    output_file=output_file_path_report,
    tools=[file_reader_tool, save_into_json],
    agent=writer_agent,
    verbose=True
)


