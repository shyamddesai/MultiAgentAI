from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, DirectoryReadTool
import os
from dotenv import load_dotenv
import time

load_dotenv()
# openai_api_key = get_openai_api_key()
# os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

file_read_tool = FileReadTool()
directory_read_tool = DirectoryReadTool("reports/categorized_news_reports/cleaned_exploration")
# file_paths = glob.glob("reports/categorized_news_reports/cleaned_exploration/*")

# ------------------------------------------------------------------------------

news_analyst = Agent(
    role="Oil and Gas Industry Information Analyst",
    goal="Extract insightful and relevant summaries for the oil and gas market, tailored for ADNOC Global Trading.",
    tools=[file_read_tool, directory_read_tool],
    backstory=(
        "You work at ADNOC Global Trading as an expert analyst in the oil and gas energy market. "
        "Your primary objective is to write analytical summaries based on all relevant documents, "
        "focusing on key insights for ADNOC Global Trading."
    ),
    verbose=True,
)

news_analyst_task = Task(
    description=(
        "First, use the directory_read_tool to list all file paths in the provided directory. "
        "Then, use the file_read_tool to read each file. Focus on the 'Content' part of each file. "
        "For each file, provide a one-line summary of the 'Content', highlighting the key insights relevant to ADNOC Global Trading."
        ),
    expected_output="A text file containing one-line summaries for each analyzed document.",
    output_file='./reports/news_report_analysis.md',
    tools=[file_read_tool, directory_read_tool],
    agent=news_analyst,
    verbose=True
)

crew = Crew(
    agents=[news_analyst],
    tasks=[news_analyst_task],
    verbose=True
)
start = time.time()
result = crew.kickoff(inputs={})
end = time.time()
print(end-start)