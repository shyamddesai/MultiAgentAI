import os
from crewai import Agent, Crew, Process, Task
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from langchain_openai import ChatOpenAI
from utils import get_openai_api_key
from dotenv import load_dotenv

# -----------------------------------------------------------------------------

input_file_path = './Data/reports/reports/report.json'
output_file_path = './Data/reports/reports/highlights.json'

# Load environment variables
load_dotenv()
openai_api_key = get_openai_api_key()
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the environment variables.")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# -----------------------------------------------------------------------------

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
                    'Ensure the output is accurate to the JSON format i.e. use square bracket, double quotation marks '
                    'to define the atrributes, commas to split attributes, does not contain the word json, no double '
                    'quotation marks at the beginning, and no unnecessary backslashes.Here is an example of the '
                    'expected JSON output: [{"Highlight Paragraph":}]',
    output_file=output_file_path,
    tools=[FileReadTool(file_path=input_file_path)],
    agent=writer_agent,
    verbose=True
)

highlight_crew = Crew(
    agents=[writer_agent],
    tasks=[writer_task],
    manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.1),
    verbose=2, # Set verbosity level for logging
    process=Process.sequential # Use sequential process for execution
)

# -----------------------------------------------------------------------------

def execute_summary_writer():
    try:
        result = highlight_crew.kickoff()
        print(f"Results saved to {output_file_path}")
        return result
    except Exception as e:
        print(f"An error occurred: {e}")