import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from rake_nltk import Rake
from urllib.parse import quote_plus, quote
import nltk
import feedparser
from datetime import datetime, timedelta
from tavily import TavilyClient
from pydantic import PrivateAttr
from crewai_tools import BaseTool, FileReadTool
import requests
from requests.exceptions import RequestException, Timeout
from typing import ClassVar, Dict


# nltk.download('stopwords')
# nlp = spacy.load("en_core_web_sm")


class SophisticatedKeywordGeneratorTool(BaseTool):
    name: str = "SophisticatedKeywordGeneratorTool"
    description: str = "This tool generates specific keywords from a given high-level topic using advanced NLP techniques."

    def _run(self, topic: str) -> list:
        # Use spaCy to process the text
        # doc = nlp(topic)

        # Extract relevant named entities
        entities = [
            "OPEC", "Oil Companies", "ADNOC", "Aramco", "SNPC", "Sonatrach",
            "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
            "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC",
            "Sinopec", "PetroChina", "GazProm", "QatarEnergy", "CNOOC",
            "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
            "ConocoPhillips", "Canadian Natural Resources",
            "TotalEnergies", "British Petroleum", "BP",  "Chevron",
            "Equinor", "Eni", "Petrobras"
        ]

        # Extract relevant noun chunks
        # noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOP_WORDS and ('oil' in chunk.text.lower() or 'gas' in chunk.text.lower())]

        # Use RAKE to extract keywords
        # rake = Rake()
        # rake.extract_keywords_from_text(topic)
        # rake_keywords = rake.get_ranked_phrases()

        # Combine all keywords
        all_keywords = entities

        specific_keywords = [
            "OPEC", "Oil Companies", "ADNOC", "Aramco", "SNPC", "Sonatrach",
            "GEPetrol", "Gabon Oil", "National Iranian Oil Company",
            "Iraq Petroleum", "Kuwait Oil Company", "PDVSA", "IEA", "APEC",
            "Sinopec", "PetroChina", "GazProm", "QatarEnergy", "CNOOC",
            "ExxonMobil", "Shell", "Marathon Petroleum", "Valero Energy",
            "ConocoPhillips", "Canadian Natural Resources",
            "TotalEnergies", "British Petroleum", "BP",  "Chevron",
            "Equinor", "Eni", "Petrobras"
            "oil prices", "gas prices", "oil stock market", "oil company",
            "oil supply", "oil demand", "oil production", "gas production",
            "energy market", "oil trading", "gas trading", "crude oil",
            "natural gas", "commodity prices", "oil futures", "gas futures",
            "oilfield services",
            "petroleum",  "LNG",
            "oil reserves", "shale oil", "oil exports", "oil imports", "OPEC",
            "oil consumption", "oil inventory", "Light Distillate", "Naphtha",  "LPG", "Biofuels",
            "Middle Distillate", "Jet Fuel", "Gas Oil",  "Condensate", "Fuel Oil and Bunker", "Brent", "WTI",
            "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil", "Gasoil", "Marine gasoil",
            "Far east index",  "Mt Belv Propane", "Mt Belv Butane", "ULSD New york",
            "UlSD", "Far east index propane", "Far east index butane", "gasoil", "europe gasoil", "asia gasoil",
            "marine gasoil", "propane", "butane", "Diesel", "Gasoline", "downstream", "upstream", "midstream", "exploration", "refining",
            "pipelines", "drilling", "trade", "market", "trend", "forecast"


        ]
        # Add domain-specific keywords
        all_keywords += specific_keywords

        # Deduplicate and filter keywords
        keywords = list(set(all_keywords))
        keywords = [kw for kw in keywords if len(kw.split()) <= 3 and len(kw) > 2]

        # Refine keywords to avoid unrelated topics
        # refined_keywords = [kw for kw in keywords if 'stock' not in kw or 'oil' in kw or 'gas' in kw]

        return keywords
    
# ------------------------------------------------------------------------------


class RSSFeedScraperTool(BaseTool):
    name: str = "RSSFeedScraperTool"
    description: str = ("This tool dynamically generates RSS feed URLs from keywords and "
                        "scrapes them to extract news articles. It returns a list of "
                        "articles with titles and links from the past week.")

    def _run(self, keywords_list: list) -> list:
        articles = []
        date_range = 7
        one_week_ago = datetime.now() - timedelta(days=date_range)

        for keyword in keywords_list:
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(keyword)}+when:{date_range}d"
            feed = feedparser.parse(rss_url)
            keyword_article_count = 0
            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:6])
                if published >= one_week_ago:
                    articles.append({
                        "Title": entry.title,
                        "Link": entry.link,
                        "Published": entry.published,
                    })
                    keyword_article_count += 1
            print(f"Keyword '{keyword}' added {keyword_article_count} articles")
        return articles

# ------------------------------------------------------------------------------


file_reader_tool = FileReadTool(file_path='C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/reports/news_report_analysis_parallel.md')

from crewai_tools import BaseTool
import requests
from requests.exceptions import RequestException, Timeout
from typing import ClassVar, Dict
import datetime


class MarketAnalysisTool(BaseTool):
    name: str = "Market Analysis Tool"
    description: str = "Analyzes market trends for a given commodity."

    # Mapping of commodity names to Quandl database codes
    commodity_symbol_mapping: ClassVar[Dict[str, str]] = {
        "Brent": "CHRIS/ICE_B1",
        "WTI": "CHRIS/CME_CL1",
        "RBOB": "CHRIS/CME_RB1",
        "EBOB": "NSE/EBOP",
        "CBOB": "NSE/CBOP",
        "Singapore gasoline R92": "SGX/FC03",
        "Europe Gasoil": "CHRIS/ICE_GASO",
        "Marine gasoil 0.5% Singapore": "SGX/MGO",
        "Far east index propane": "EIA/PET_WCRSTUS1",
        "Far east index butane": "EIA/PET_WRBSTUS1",
        "Mt Belv Propane": "EIA/PET_RTPM_NUS_D",
        "Mt Belv Butane": "EIA/PET_RTBU_NUS_D",
        "ULSD New york": "EIA/PET_RMLS_NUS_D",
        "asia gasoil": "SGX/FOIL",
        "marine gasoil": "SGX/MGO",
        "Gold": "LBMA/GOLD",
        "Silver": "LBMA/SILVER"
    }

    def _run(self, commodity: str):
        # Fetch the correct code for the commodity
        code = self.commodity_symbol_mapping.get(commodity)
        if not code:
            return f"No code mapping found for {commodity}."

        # Fetching market data from Quandl API
        api_key = "ush97YpzsUyRTDZX8kWp"  # Replace with your Quandl API key
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.datetime.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')  # Last 30 days
        api_endpoint = f"https://www.quandl.com/api/v3/datasets/{code}/data.json?api_key={api_key}"

        try:
            response = requests.get(api_endpoint, timeout=10)  # Set a timeout for the request
            response.raise_for_status()  # Raise an error for bad status codes
            market_data = response.json()
            return self.analyze_market_data(commodity, market_data)
        except Timeout:
            return f"Request to Quandl API timed out for {commodity}."
        except RequestException as e:
            return f"An error occurred while fetching market data for {commodity}: {e}"

    def analyze_market_data(self, commodity: str, market_data: Dict):
        # Basic analysis example: Checking for bullish or bearish trend
        data = market_data.get("dataset_data", {}).get("data", [])
        if not data:
            return "No data available for analysis."

        latest_data = data[0]
        price = latest_data[1]  # Assuming the price is the second element in the data array
        prices = [entry[1] for entry in data]
        moving_average = self.calculate_moving_average(prices)

        if price > moving_average:
            trend = "bullish"
        else:
            trend = "bearish"

        # Dummy sentiment analysis (replace with actual sentiment analysis)
        # sentiment_analysis = "positive" if price > moving_average else "negative"

        analysis = (
            f"Market Analysis for {commodity}:\n"
            f"- Current Price: {price}\n"
            f"- Moving Average: {moving_average}\n"
            f"- Trend: {trend}\n"
            # f"- Market Sentiment: {sentiment_analysis}\n"
        )
        return analysis

    def calculate_moving_average(self, prices: list, window: int = 20) -> float:
        if len(prices) < window:
            return sum(prices) / len(prices)
        return sum(prices[:window]) / window

    def __call__(self, commodity: str) -> str:
        return self._run(commodity)


market_analysis_tool = MarketAnalysisTool()


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