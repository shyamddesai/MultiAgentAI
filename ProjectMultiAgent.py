import warnings
from crewai import Agent, Task, Crew, Process
import os
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, XMLSearchTool
from IPython.display import Markdown
import json
from pydantic import BaseModel, PrivateAttr
from utils import get_openai_api_key
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai_tools import BaseTool

warnings.filterwarnings('ignore')

# Define a Pydantic model for news details
# class NewsDetails(BaseModel):
#     Link: str
#     Title: str
#     # Summary: str

#define xml reading file tool
xml_tool = XMLSearchTool(xml='./RSS/GoogleNews.xml')

#define scraping tool
scrape_tool = ScrapeWebsiteTool()
# Define TavilyAPI tool
class TavilyAPI(BaseTool):
    name: str = "TavilyAPI"
    description: str = ("The best search engine to use. If you want to search for anything, USE IT! "
                        "Make sure your queries are very specific or else you will "
                        "get websites that have the same content and that will waste your time.")

    _client: TavilyClient = PrivateAttr()

    def __init__(self, api_key: str):
        super().__init__()
        self._client = TavilyClient(api_key=api_key)

    def _run(self, query: str) -> list:
        response = self._client.search(query=query, search_depth='basic', max_results=100)
        results = [{"Link": result["url"], "Title": result["title"]} for result in response["results"]]
        return results

# Define NewsSaver tool
# class NewsSaver(BaseTool):
#     name: str = "NewsSaver"
#     description: str = "Saves the provided news data into a JSON file."
#
#     def _run(self, news_data: list) -> str:
#         try:
#             with open('news_report.json', 'w') as f:
#                 json.dump(news_data, f, indent=2)
#             return "News data successfully saved to news_report.json."
#         except Exception as e:
#             return f"Failed to save news data: {e}"


# Load environment variables from .env file
load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialize the TavilyAPI tool
tavily_tool = TavilyAPI(api_key=tavily_api_key)

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# docs_scrape_tool = ScrapeWebsiteTool(
#     website_url="https://www.worldoil.com/news/2024/6/23/adnoc-extends-vallourec-s-900-million-oil-and-gas-tubing-contract-to-2027/"
# )

# Define agents
news_researcher = Agent(
    role="Elite News Aggregator",
    goal="Provide a list of URLs that include relevant news articles on: {topics}.",
    tools=[tavily_tool, xml_tool],
    backstory="You are an elite news aggregator with a deep understanding of global events and trends. "
              "Your expertise lies in sifting through vast amounts of information to find the most pertinent and timely news URLS."
              " You excel at identifying stories that cover a wide range of perspectives, ensuring that your list are comprehensive and balanced."
              " Your role is crucial in providing URLS for analysts and decision-makers.",
    verbose=True,

)

# news_saver = Agent(
#     role="News Saver",
#     goal="Save the provided news URLS into a JSON file.",
#     backstory="You are responsible for saving the news URLS collected by the Researcher agent into a structured format.",
#     verbose=True,
#     memory=True,
# )

# Define tasks
research_task = Task(
    description=(
        "Your mission is to gather a diverse and comprehensive set of URLS on each of the specified list of topics: {topics}. "
        "Focus on finding the most recent URL articles from reputable sources that provide different perspectives on the topics. "
        "Ensure that the information is up-to-date and relevant, covering various aspects such as political developments, technological advancements, regulatory changes, and market dynamics. "
        "Avoid redundant information by ensuring that each article adds unique value to the overall understanding of the topics."
        "USE ALL TOOLS POSSIBLE."
    ),
    expected_output='A list of All the urls that contain articles saved into a JSON type file with Link and Title.',
    #output_json=NewsDetails,
    output_file='news_report.json',
    agent=news_researcher
)

# save_task = Task(
#     description="Save the provided news URLs from Elite News Aggregator into a JSON type file.",
#     expected_output='Confirmation that the news URLS has been saved stating Link and Title.',
#     agent=news_saver
# )

# Define crew
crew = Crew(
    agents=[news_researcher],
    tasks=[research_task],
    # manager_llm=ChatOpenAI(model="gpt-4", temperature=0.7),
    process=Process.sequential,  # Ensure tasks are executed in sequence
    verbose=True
)

topics = [
    "oil and gas market", "oilfield market", "petroleum market",
    "energy market"
]

# Execute crew
result = crew.kickoff(inputs={"topics": topics})



# Display the result from the saving task
print(result)

# Load and display the saved JSON file
# with open('news_report.json') as f:
#     data = json.load(f)
#
# Markdown(json.dumps(data, indent=2))
