import warnings
from crewai import Agent, Task, Crew, Process
import os
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, XMLSearchTool
from IPython.display import Markdown
import json
from pydantic import BaseModel, PrivateAttr
from textblob import TextBlob
from utils import get_openai_api_key, get_serper_api_key
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai_tools import BaseTool

warnings.filterwarnings('ignore')

# Define a Pydantic model for news details
# class NewsDetails(BaseModel):
#     Link: str
#     Title: str
#     # Summary: str

#define tools

# docs_scrape_tool = ScrapeWebsiteTool(
#     website_url="https://www.worldoil.com/news/2024/6/23/adnoc-extends-vallourec-s-900-million-oil-and-gas-tubing-contract-to-2027/"
# )

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

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-4'
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

serper_api_key=get_serper_api_key()
os.environ["SERPER_API_KEY"] = serper_api_key


xml_tool = XMLSearchTool(xml='./RSS/GoogleNews.xml')

serper_tool = SerperDevTool()

scrape_tool = ScrapeWebsiteTool()

class SentimentAnalysisTool(BaseTool):
    name: str = "SentimentAnalysisTool"
    description: str = "This tool analyzes the sentiment of a given text and returns the sentiment polarity and subjectivity. Useful for evaluating the tone and mood of news articles."

    def _run(self, text: str) -> str:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        return f"Polarity: {polarity}, Subjectivity: {subjectivity}"

# Define the sentiment analysis tool
sentiment_tool = SentimentAnalysisTool()

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

# Initialize the TavilyAPI tool
tavily_tool = TavilyAPI(api_key=tavily_api_key)

# Define the News Gatherer Agent
news_gatherer = Agent(
    role="News Gatherer",
    goal="To collect and compile a comprehensive list of URLs and titles "
         "from various news sources and RSS feeds related to specified topics in the energy market.",
    tools=[serper_tool, scrape_tool, xml_tool,tavily_tool],
    backstory="You are a dedicated and meticulous web crawler and aggregator, "
              "driven by a passion for information and data organization. "
              "Your skills in digital journalism and data scraping enable you "
              "to efficiently gather relevant news URLs from diverse sources.",
    allow_delegation=False,
    verbose=True,
)

content_analyzer = Agent(
    role="Content Analyzer",
    goal="To filter and analyze the collected articles to determine their relevance "
         "and importance based on specified topics and criteria.",
    tools=[sentiment_tool],
    backstory="You are a skilled analyst with a keen eye for identifying significant "
              "and relevant information within large sets of data. Your expertise in "
              "content analysis and relevance filtering ensures that only the most valuable "
              "articles are highlighted.",
    allow_delegation=False,
    verbose=True,
)

# Define the task for analyzing content
content_analysis_task = Task(
    description=(
        "Analyze the collected articles to determine their relevance and importance based on the specified topics. "
        "Use natural language processing (NLP) and sentiment analysis to evaluate each article. "
        "Filter out articles that are not relevant or do not provide significant insights. "
        "Your goal is to create a curated list of the most important and relevant articles on: {topics}."
    ),
    expected_output="A filtered list of articles with their relevance scores. Each entry should include the URL, title, and relevance score.",
    output_file='filtered_news_report.json',
    agent=content_analyzer
)


# news_saver = Agent(
#     role="News Saver",
#     goal="Save the provided news URLS into a JSON file.",
#     backstory="You are responsible for saving the news URLS collected by the Researcher agent into a structured format.",
#     verbose=True,
#     memory=True,
# )

# Define tasks
# Define the task for gathering news
news_gathering_task = Task(
    description=(
        "Collect a comprehensive list of URLs and their titles from various news sources,"
        " websites, and RSS feeds. Ensure that the URLs are current, relevant, and cover "
        "a wide range of perspectives. Your goal is to gather a diverse set of links that "
        "provide the latest updates and insights on: {topics}. Each collected "
        "entry should include the URL and the title of the corresponding article or news piece."
    ),
    expected_output="A JSON file containing a list of the collected URLs and their titles. "
                    "Each entry in the list should be a dictionary with two keys: 'Link' "
                    "for the URL and 'Title' for the article's title. The final output should "
                    "reflect a wide range of sources and perspectives, ensuring the information "
                    "is current and relevant.",
    output_file='news_report.json',
    agent=news_gatherer
)

# save_task = Task(
#     description="Save the provided news URLs from Elite News Aggregator into a JSON type file.",
#     expected_output='Confirmation that the news URLS has been saved stating Link and Title.',
#     agent=news_saver
# )

# Define the crew
crew = Crew(
    agents=[news_gatherer],
    tasks=[news_gathering_task],
    process=Process.sequential,  # Ensure tasks are executed in sequence
    verbose=True,
    memory=True
)


topics = [
    "Renewable Energy ", "Green Energy Initiatives", "Energy Transition",
    "Crude Oil Prices",'LNG Market', 'Carbon Emissions', 'Energy Policy',
    'Climate Change Impact','Energy Infrastructure','Power Generation',
    'Energy Security','Global Energy Markets','Energy Supply Chain',
    'Oil Refining',"Fuel Efficiency"
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
