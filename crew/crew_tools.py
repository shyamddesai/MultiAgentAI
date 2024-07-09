import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from rake_nltk import Rake
from urllib.parse import quote_plus
import nltk
import feedparser
from datetime import datetime, timedelta
from tavily import TavilyClient
from pydantic import PrivateAttr
from crewai_tools import BaseTool

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
            "TotalEnergies", "British Petroleum (or BP)", "Chevron",
            "Equinor", "Eni", "Petrobras"
        ]

        # Extract relevant noun chunks
        # noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOP_WORDS and ('oil' in chunk.text.lower() or 'gas' in chunk.text.lower())]

        # Use RAKE to extract keywords
        rake = Rake()
        rake.extract_keywords_from_text(topic)
        rake_keywords = rake.get_ranked_phrases()

        # Combine all keywords
        all_keywords = entities + rake_keywords

        # Add domain-specific keywords
        specific_keywords = [
            "oil prices", "gas prices", "oil stock market", "oil company",
            "oil supply", "oil demand", "oil production", "gas production",
            "energy market", "oil trading", "gas trading", "crude oil",
            "natural gas", "commodity prices", "oil futures", "gas futures",
            "exploration", "refining", "pipelines", "oilfield services",
            "petroleum", "downstream", "upstream", "midstream", "LNG",
            "oil reserves", "drilling", "shale oil",
            "oil exports", "oil imports", "OPEC",
            "oil consumption", "oil inventory",
            "Light Distillate", "Naphtha", "Gasoline", "LPG", "Biofuels", "Middle Distillate",
            "Jet Fuel", "Gas Oil", "Diesel", "Condensate", "Fuel Oil and Bunker", "Brent", "WTI",
            "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil", "Gasoil", "Marine gasoil",
            "Far east index", "propane", "butane", "Mt Belv Propane", "Mt Belv Butane", "ULSD New york",
            "UlSD"
        ]
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
        one_week_ago = datetime.now() - timedelta(days=3)

        for keyword in keywords_list:
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(keyword)}+when:3d"
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