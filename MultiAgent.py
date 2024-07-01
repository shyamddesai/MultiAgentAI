import warnings
from crewai import Agent, Task, Crew, Process
import os

from crewai_tools.tools.xml_search_tool.xml_search_tool import XMLSearchTool
from langchain_openai import ChatOpenAI
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
import feedparser
from urllib.parse import quote_plus
import spacy
import nltk
from rake_nltk import Rake
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from datetime import datetime, timedelta
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

# define scraping tool
# scrape_tool = ScrapeWebsiteTool("https://news.google.com/rss/search?q=Renewable+Energy",
# "https://news.google.com/rss/search?q=Green+Energy+Initiatives",
#     "https://news.google.com/rss/search?q=Energy+Transition",
#     "https://news.google.com/rss/search?q=Crude+Oil+Prices",
#     "https://news.google.com/rss/search?q=LNG+Market",
#     "https://news.google.com/rss/search?q=Carbon+Emissions",
#     "https://news.google.com/rss/search?q=Energy+Policy",
#     "https://news.google.com/rss/search?q=Climate+Change+Impact",
#     "https://news.google.com/rss/search?q=Energy+Infrastructure",
#     "https://news.google.com/rss/search?q=Power+Generation",
#     "https://news.google.com/rss/search?q=Energy+Security",
#     "https://news.google.com/rss/search?q=Global+Energy+Markets",
#     "https://news.google.com/rss/search?q=Energy+Supply+Chain",
#     "https://news.google.com/rss/search?q=Oil+Refining",
#     "https://news.google.com/rss/search?q=Fuel+Efficiency"
# )

# Define TavilyAPI tool

nltk.download('stopwords')
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


class SophisticatedKeywordGeneratorTool(BaseTool):
    name: str = "SophisticatedKeywordGeneratorTool"
    description: str = "This tool generates specific keywords from a given high-level topic using advanced NLP techniques."

    def _run(self, topic: str) -> list:
        # Use spaCy to process the text
        doc = nlp(topic)

        # Extract named entities
        entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "PRODUCT", "EVENT"]]

        # Extract noun chunks and important words
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOP_WORDS]
        words = [token.text for token in doc if token.is_alpha and token.text.lower() not in STOP_WORDS]

        # Use RAKE to extract keywords
        rake = Rake()
        rake.extract_keywords_from_text(topic)
        rake_keywords = rake.get_ranked_phrases()

        # Combine all keywords
        all_keywords = entities + noun_chunks + words + rake_keywords

        # Add specific keywords related to the oil and gas market, stock prices, supply and demand
        specific_keywords = ["oil prices", "gas prices", "stock market", "oil company news", "supply and demand",
                             "production rates", "customer demand", "trading news"]
        all_keywords += specific_keywords

        # Deduplicate and filter keywords
        keywords = list(set(all_keywords))
        keywords = [kw for kw in keywords if len(kw.split()) <= 3 and len(kw) > 2]

        return keywords


# Define the RSSFeedScraperTool
class RSSFeedScraperTool(BaseTool):
    name: str = "RSSFeedScraperTool"
    description: str = ("This tool dynamically generates RSS feed URLs from keywords and "
                        "scrapes them to extract news articles. It returns a list of "
                        "articles with titles and links from the past week.")

    def _run(self, keywords: list) -> list:
        articles = []
        one_week_ago = datetime.now() - timedelta(days=7)
        for keyword in keywords:
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(keyword)}+when:7d"
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:6])
                if published >= one_week_ago:
                    articles.append({
                        "Title": entry.title,
                        "Link": entry.link,
                        "Published": entry.published
                    })
        return articles


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

serper_api_key = os.getenv("SERPER_API_KEY")
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

# scrape website
docs_scrape_tool = ScrapeWebsiteTool(
    # website_url="https://www.worldoil.com/news/2024/6/23/adnoc-extends-vallourec-s-900-million-oil-and-gas-tubing-contract-to-2027/"
)
# Define the keyword generator and RSS feed scraper tools
keyword_generator = SophisticatedKeywordGeneratorTool()
rss_feed_scraper = RSSFeedScraperTool()

# Define the News Gatherer Agent
news_gatherer = Agent(
    role="News Gatherer",
    goal="To collect and compile a comprehensive list of URLs and titles "
         "from various news sources and RSS feeds related to specified topics in the energy market.",
    tools=[keyword_generator, rss_feed_scraper],
    backstory="You are a dedicated and meticulous web crawler and aggregator, "
              "driven by a passion for information and data organization. "
              "Your skills in digital journalism and data scraping enable you "
              "to efficiently gather relevant news URLs from diverse sources.",
    allow_delegation=False,
    verbose=False,
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

news_gathering_task = Task(
    description=(
        "Generate specific keywords from the given topic and use these keywords to dynamically generate RSS feed URLs. "
        "Scrape these feeds to collect a comprehensive list of URLs and their titles from various news sources from the past week. "
        "Ensure that the URLs are current, relevant, and cover a wide range of perspectives. "
        "Your goal is to gather a diverse set of links that provide the latest updates and insights on the given topic, particularly focusing on stock prices, "
        "news related to the oil and gas industry, factors affecting supply and demand, production rates, and customer demand. "
        "Each collected entry should include the URL, the title of the corresponding article or news piece, and the publication date."
    ),
    expected_output="A JSON file containing a list of the collected URLs, their titles, and publication dates. "
                    "Each entry in the list should be a dictionary with three keys: 'Link' for the URL, 'Title' for the article's title, and 'Published' for the publication date. "
                    "The final output should reflect a wide range of sources and perspectives, ensuring the information is current and relevant.",
    output_file='news_report.json',
    agent=news_gatherer
)



analysis_task = Task(
    description=(
        "Analyze the gathered news articles from the News Researcher and identify key "
        "trends and insights in topic:{topic}. Summarize the information in a concise manner."
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
    agents=[news_gatherer],
    tasks=[news_gathering_task],
    # manager_llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7),
    process=Process.sequential,
    verbose=False
)

# Input topic
topic = "latest news on oil and gas market and its impact on stock prices, supply and demand, and production rates"


result = crew.kickoff(inputs={"topic": topic})

