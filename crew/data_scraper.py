from crewai import Agent, Task
from crew import SophisticatedKeywordGeneratorTool, RSSFeedScraperTool
import os
from utils import get_openai_api_key
from dotenv import load_dotenv

load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# ------------------------------------------------------------------------------

# Define the News Gatherer Agent
news_gatherer = Agent(
    role="News Gatherer",
    goal="To collect and compile a comprehensive list of URLs and titles "
         "from various news sources and RSS feeds related to specified topics in the energy market.",
    tools=[SophisticatedKeywordGeneratorTool(), RSSFeedScraperTool()],
    backstory="You are a dedicated and meticulous web crawler and aggregator, "
              "driven by a passion for information and data organization. "
              "Your skills in digital journalism and data scraping enable you "
              "to efficiently gather relevant news URLs from diverse sources.",
    allow_delegation=False,
    verbose=False,
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
                    "Each entry in the list should be a dictionary with 2 keys: 'Link' for the URL, 'Title' for the article's title. "
                    "The final output should reflect a wide range of sources and perspectives, ensuring the information is current and relevant.",
    output_file='news_report.json',
    agent=news_gatherer
)