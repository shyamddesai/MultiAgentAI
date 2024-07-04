import warnings
from crewai import Agent, Task, Crew, Process
import os
from collections import defaultdict
from difflib import SequenceMatcher
from crewai_tools.tools.xml_search_tool.xml_search_tool import XMLSearchTool
from langchain_openai import ChatOpenAI
# from utils import get_openai_api_key
from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
import requests
import time
import aiohttp
import asyncio
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

from crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, TavilyAPI, filter_articles_async, 
                  group_articles_by_category, news_gatherer, news_gathering_task, news_analyst, analysis_task)

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

crew = Crew(
    agents=[news_gatherer],
    tasks=[news_gathering_task],
    # manager_llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7),
    process=Process.sequential,
    verbose=False
)

# Input topic
topic = " oil and gas market latest news, oil and gas stock prices, oil and gas supply and demand, and oil and gas production rates"

# Execute the crew with the input topic
keywords = SophisticatedKeywordGeneratorTool()._run(topic)
result = RSSFeedScraperTool()._run(keywords)

# print(result)

# Specify the output file path
output_file = './reports/news_report.json'

# Save the result to the specified output file
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)


# result = crew.kickoff(inputs={"topic": topic})

# Load articles from JSON file
with open('./reports/news_report.json', 'r') as f:
    articles = json.load(f)

# Define relevant keywords
relevant_keywords = [
    "oil prices", "gas prices", "oil stock market", "oil company",
    "oil supply", "oil demand", "oil production", "gas production",
    "energy market", "oil trading", "gas trading", "crude oil",
    "natural gas", "commodity prices", "oil futures", "gas futures",
    "exploration", "refining", "pipelines", "oilfield services",
    "petroleum", "downstream", "upstream", "midstream", "LNG",
    "oil reserves", "drilling", "shale oil", "offshore drilling",
    "oil exports", "oil imports", "OPEC", "oil refining capacity",
    "oil production cuts", "oil consumption", "oil inventory"
]

# Define categories and their corresponding keywords
categories = {
    "Market Trends": ["market", "trend", "forecast"],
    "Production Updates": ["production", "output", "supply", "production rates"],
    "Company News": ["company", "merger", "acquisition", "oil company"],
    "Stock Prices": ["stock prices", "oil stock market", "commodity prices", "oil futures", "gas futures"],
    "Supply and Demand": ["supply", "demand", "oil supply", "oil demand", "gas supply", "gas demand"],
    "Exploration": ["exploration", "drilling", "shale oil", "offshore drilling"],
    "Refining": ["refining", "oil refining capacity", "oil production cuts", "oil inventory"],
    "Trade and Export": ["trading", "export", "import", "oil exports", "oil imports"]
}

# Filter articles for redundancy, relevancy, and categorize them
filtered_articles = asyncio.run(filter_articles_async(articles, relevant_keywords, categories, relevancy_threshold=3))

# Group articles by category
grouped_articles = group_articles_by_category(filtered_articles)

# Save each category's articles to separate JSON files
output_dir = './reports/categorized_news_reports'
os.makedirs(output_dir, exist_ok=True)

for category, articles in grouped_articles.items():
    category_file = os.path.join(output_dir, f'{category.replace(" ", "_").lower()}_news_report.json')
    with open(category_file, 'w') as f:
        json.dump(articles, f, indent=2)

print(f"Filtered and categorized articles saved to separate files in '{output_dir}'")




