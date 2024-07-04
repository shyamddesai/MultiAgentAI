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

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

class SophisticatedKeywordGeneratorTool(BaseTool):
    name: str = "SophisticatedKeywordGeneratorTool"
    description: str = "This tool generates specific keywords from a given high-level topic using advanced NLP techniques."

    def _run(self, topic: str) -> list:
        # Use spaCy to process the text
        doc = nlp(topic)

        # Extract relevant named entities
        entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "PRODUCT", "EVENT"] and ('oil' in ent.text.lower() or 'gas' in ent.text.lower())]

        # Extract relevant noun chunks
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOP_WORDS and ('oil' in chunk.text.lower() or 'gas' in chunk.text.lower())]

        # Use RAKE to extract keywords
        rake = Rake()
        rake.extract_keywords_from_text(topic)
        rake_keywords = rake.get_ranked_phrases()

        # Combine all keywords
        all_keywords = entities + noun_chunks + rake_keywords

        # Add domain-specific keywords
        specific_keywords = [
            "oil prices", "gas prices", "oil and gas stock market", "oil company news",
            "oil and gas supply and demand", "oil production rates", "gas production rates",
            "energy market news", "oil trading news", "gas trading news", "crude oil prices",
            "natural gas prices", "commodity prices", "oil futures", "gas futures",
            "exploration", "refining", "pipelines", "oilfield services", "petroleum",
            "downstream", "upstream", "midstream", "LNG", "oil reserves", "drilling",
            "shale oil", "offshore drilling", "oil exports", "oil imports", "OPEC",
            "oil refining capacity", "oil production cuts", "oil consumption", "oil inventory"
        ]
        all_keywords += specific_keywords

        # Deduplicate and filter keywords
        keywords = list(set(all_keywords))
        keywords = [kw for kw in keywords if len(kw.split()) <= 3 and len(kw) > 2]

        # Refine keywords to avoid unrelated topics
        refined_keywords = [kw for kw in keywords if 'stock' not in kw or 'oil' in kw or 'gas' in kw]

        return refined_keywords
    
# ------------------------------------------------------------------------------
    
class RSSFeedScraperTool(BaseTool):

    name: str = "RSSFeedScraperTool"
    description: str = ("This tool dynamically generates RSS feed URLs from keywords and "
                        "scrapes them to extract news articles. It returns a list of "
                        "articles with titles and links from the past week.")

    def _run(self, refined_keywords: list) -> list:
        articles = []
        one_week_ago = datetime.now() - timedelta(days=3)
        for refined_keyword in refined_keywords:
            rss_url = f"https://news.google.com/rss/search?q={quote_plus(refined_keyword)}+when:3d"
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                published = datetime(*entry.published_parsed[:6])
                if published >= one_week_ago:
                    articles.append({
                        "Title": entry.title,
                        "Link": entry.link,
                        "Published": entry.published,

                    })
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