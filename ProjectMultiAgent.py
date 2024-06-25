import warnings
from crewai import Agent, Task, Crew, Process
import os
from langchain_openai import ChatOpenAI
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
#which markets ADNOC interested in and trade in, where are the news about these markets,
from IPython.display import Markdown

warnings.filterwarnings('ignore')


# openai_api_key = get_openai_api_key()
# os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

docs_scrape_tool = ScrapeWebsiteTool(
    # website_url="https://www.worldoil.com/news/2024/6/23/adnoc-extends-vallourec-s-900-million-oil-and-gas-tubing-contract-to-2027/"
)

news_researcher = Agent(
    role="Senior News Researcher",
    goal="Collect relevant and up-to-date news regarding on: {topic}",
    backstory="You're working on collecting live news  "
              "about this topic. You have to include all the news that affect this market"
              "Information from politics, technology advancements, regulatory changes, and "
              "operational/logistical changes "
              "that are relevant to this market."
              "The data you will collect will be given to the Analyst "
              "and will be the basis for "
              "the Analyst to make an analysis on this topic.",

	verbose=True,
    memory=True,
    tools=[docs_scrape_tool],
)

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

research_task = Task (
    description=(
        "Gather news articles and relevant information on the specified topic:{topic} from various sources. "
        "Ensure that the information is up-to-date and covers different perspectives."
    ),
    expected_output='List of the summarized relevant news articles with their sources.',
    agent=news_researcher
)

analysis_task = Task(
    description=(
        "Analyze the gathered news articles from the News Researcher and identify key trends and insights in topic:{topic}. "
        "Summarize the information in a concise manner."
    ),
    expected_output='A summary report highlighting the key trends and insights from the analyzed news articles.',
    agent=news_analyst
)

editing_task = Task(
    description=(
        "Compile the analyzed information into a well-structured report. "
        "Ensure that the report is clear, engaging, and free of errors."
    ),
    expected_output='A final report in markdown format that is well-structured and engaging.',
    agent=writer
)

crew = Crew(
    agents=[news_researcher, news_analyst, writer],
    tasks=[research_task, analysis_task, editing_task],

    manager_llm=ChatOpenAI(model="gpt-3.5-turbo",
                           temperature=0.7),
    process=Process.hierarchical,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "oil and gas market"})
Markdown(result)











