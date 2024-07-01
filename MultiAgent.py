import warnings
from crewai import Agent, Task, Crew, Process
import os

from crewai_tools.tools.xml_search_tool.xml_search_tool import XMLSearchTool
from langchain_openai import ChatOpenAI
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
#which markets ADNOC interested in and trade in, where are the news about these markets,
from IPython.display import Markdown
import json
from pydantic import BaseModel, PrivateAttr
from utils import get_openai_api_key
from dotenv import load_dotenv
from tavily import TavilyClient
from crewai_tools import BaseTool

# Define a Pydantic model for news details
# class NewsDetails(BaseModel):
#     Link: str
#     Title: str
#     Summary: str

# Load environment variables from .env file

warnings.filterwarnings('ignore')

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

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
        response = self._client.search(query=query, search_depth='basic', max_results=10)
        results = [{"Link": result["url"], "Title": result["title"]} for result in response["results"]]
        return results


load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

serper_tool = SerperDevTool()
# Initialize the TavilyAPI tool
tavily_tool = TavilyAPI(api_key=tavily_api_key)

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


docs_scrape_tool = ScrapeWebsiteTool(
    # website_url="https://www.worldoil.com/news/2024/6/23/adnoc-extends-vallourec-s-900-million-oil-and-gas-tubing-contract-to-2027/"
)

# Define the News Gatherer Agent
news_gatherer = Agent(
    role="News Gatherer",
    goal="To collect and compile a comprehensive list of URLs and titles "
         "from various news sources and RSS feeds related to specified topics in the energy market.",
         
    tools=[scrape_tool, xml_tool],
    backstory="You are a dedicated and meticulous web crawler and aggregator, "
              "driven by a passion for information and data organization. "
              "Your skills in digital journalism and data scraping enable you "
              "to efficiently gather relevant news URLs from diverse sources.",
    allow_delegation=False,
    verbose=True,
)


news_analyst = Agent(
    role="Oil and Gas Industry Expert News Analyst",
    goal="Extract insightful information based on what is relevant to the oil and gas market that is extracted by the Elite News Aggregator",
    tools=[scrape_tool],
    backstory="You're working at ADNOC Global Trading as an expert analyst in the oil and gas energy market."
              "You want to write an analytical piece for each of the articles that is relevant to ADNOC. "
              "You base your writing on the work of "
              "the Elite News Aggregator, who provides the relevant links  "
              " about the topic. "
              "You also provide accurate strategies and advice with a focus on stock updates like WTI Crude and Brent Crude "
              "and back them up with information like relevant technological breakthroughs and events in the geopolitical environment. "
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
                    "Each entry in the list should be a dictionary with three keys: 'Link' "
                    "for the URL and 'Title' for the article's title and 'Summary' for the "
                    "article's summary. The final output should reflect a wide range of sources"
                    " and perspectives, ensuring the information is current and relevant."
                    "Do not include the markdown ``` in the file.",
    output_file='news_report.json',
    agent=news_gatherer
)


news_analyst_task = Task(
    # description=(
    #     "Your task is to analyze and filter out the articles given to you by the Elite News Aggregator."
    #     "Visit the URLs provided and read the article on the website."
    #     "If the website isn't loading correctly, or requires a subscription to access the page, then ignore the link and move on to the next article."
    #     "Your aim is tailor this for ADNOC Global Trading, who specializes in the trade of refined products."
    #     "Embrace your role and backstory as a expert analyst and make sure the analysis you provide is relevant and insightful to the topics and ADNOC."
    description=(
        "Your task is to analyze and filter out the articles given to you by the Elite News Aggregator."
        "Visit the URLs provided and read the article on the website."
        "If the website isn't loading correctly, or requires a subscription to access the page, then ignore the link and move on to the next article."
        "Your aim is tailor this for ADNOC Global Trading, who specializes in the trade of refined products."
        "Group articles together by similarity based on the following categories: incidents and geopoltical news related to the oil and gas market, "
        "stock-related updates for WTI Crude, Brent Crude, IFAD Murban, ICE Brent, NYMEX WTI, Naphtha, Gasoline, Gasoil 10ppm, Jet Kero, and whatever other stock are relevant to the use case. "
        "Technological breakthroughs, and currency-related news."
        "Perform one analysis for each group of articles."
        "Provide trading strategies if possible based on the "
        "Embrace your role and backstory as a expert analyst and make sure the analysis you provide is relevant and insightful to the topics and ADNOC."
    ),
    expected_output = "The complete analysis for each of the groupings you deem to be appropriate from the Elite News Aggregator."
                      "Each grouping to have its own analysis separated."
                      "Provide only the overall analysis for each grouping, but cite the articles as sources",

    # expected_output = "A summary analysis of all the relevant articles/news you deem to be appropraite from the Elite News Aggregator."
    #                   "Each article to have its own analysis seperated.",
    # expected_output="A JSON file containing the list of the collected URLs and their titles from the Elite News Aggregator. "
    #                 "Each entry in the list should be a dictionary with two keys: 'Link' "
    #                 "for the URL and 'Title' for the article's title and 'Summary' for the "
    #                 "expert's analysis. "
    #                 "If an article was skipped over and so has no analysis, explain it in the summary field.",
    output_file='news_report_analysis.json',
    agent=news_analyst

)

editing_task = Task(
    description=(
        "Compile the analyzed information into a well-structured report. "
        "Ensure that the report is clear, engaging, and free of errors."
    ),
    expected_output='A final report in JSON format that is well-structured and engaging.',
    agent=writer
)

crew = Crew(
    agents=[news_gatherer, news_analyst],
    tasks=[news_gathering_task, news_analyst_task],

    #manager_llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7),
    process=Process.sequential,
    verbose=True
)

topics = [
    "Renewable Energy ", "Green Energy Initiatives", "Energy Transition",
    "Crude Oil Prices",'LNG Market', 'Carbon Emissions', 'Energy Policy',
    'Climate Change Impact','Energy Infrastructure','Power Generation',
    'Energy Security','Global Energy Markets','Energy Supply Chain',
    'Oil Refining',"Fuel Efficiency"
]


result = crew.kickoff(inputs={"topics": topics})

print(result)