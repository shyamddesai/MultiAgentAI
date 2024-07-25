import json

from crewai import Agent, Task
import os

from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from utils import get_openai_api_key
from dotenv import load_dotenv
from crewai_tools import BaseTool

# -----------------------------------------------------------------------------
# Define file paths
input_file_path = './Data/reports/reports/report.json'
output_file_path = './Data/reports/reports/highlights.json'

# Load environment variables
load_dotenv()
openai_api_key = get_openai_api_key()
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the environment variables.")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


# Initialize FileReadTool
file_reader_tool = FileReadTool(file_path=input_file_path)


# Define the writer agent
writer_agent = Agent(
    role='Summary Writer',
    goal='Generate a comprehensive summary from provided content using the read file tool',
    backstory="""You are a skilled Summary Writer, known for your ability to transform content into polished,
                comprehensive summarized paragraphs. You excel at identifying key points and presenting them in a clear
                , organized paragraph.""",
    verbose=True,
    allow_delegation=False
)

# Define the task for the writer agent
writer_task = Task(
    description="""Read and summarize the keypoints of each article into one paragraph called Highlights""",
    expected_output=" One paragraph that grabs all the highlights of the articles"
                    'Here is an example of the expected JSON output: [{"Highlights":}]',
    output_file=output_file_path,
    tools=[file_reader_tool],
    agent=writer_agent,
    verbose=True
)


