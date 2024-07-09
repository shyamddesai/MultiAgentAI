from spacy.lang.en.stop_words import STOP_WORDS
from datetime import datetime, timedelta
from tavily import TavilyClient
from pydantic import PrivateAttr
import spacy
from rake_nltk import Rake
import feedparser
from crewai_tools import BaseTool
import nltk

import os
import re
import time
from difflib import SequenceMatcher
import json
import requests
from collections import defaultdict

topic = "oil and gas market latest news, oil and gas stock prices, oil and gas supply and demand, and oil and gas production rates"

relevant_keywords = [
    "oil prices", "gas prices", "oil stock market", "oil company",
    "oil supply", "oil demand", "oil production", "gas production",
    "energy market", "oil trading", "gas trading", "crude oil",
    "natural gas", "commodity prices", "oil futures", "gas futures",
    "exploration", "refining", "pipelines", "oilfield services",
    "petroleum", "downstream", "upstream", "midstream", "LNG",
    "oil reserves", "drilling", "shale oil",
    "oil exports", "oil imports", "OPEC",
    "oil consumption", "oil inventory",
    "Light Distillate", "Naphtha", "Gasoline", "LPG", "Biofuels",
    "Middle Distillate", "Jet Fuel", "Gas Oil", "Diesel", "Condensate",
    "Fuel Oil and Bunker"
]

categories = {
    "Market Trends": ["market", "trend", "forecast"],
    "Production Updates": ["production", "output", "supply", "production rates"],
    "Company News": ["company", "merger", "acquisition", "oil company"],
    "Stock Prices": ["stock prices", "oil stock market", "commodity prices", "oil futures", "gas futures"],
    "Supply and Demand": ["supply", "demand", "oil supply", "oil demand", "gas supply", "gas demand"],
    "Exploration": ["exploration", "drilling", "shale oil", "offshore drilling"],
    "Refining": ["refining", "oil refining capacity", "oil production cuts", "oil inventory"],
    "Commodities": ["Light Distillate", "Naphtha", "Gasoline", "LPG", " Biofuels", "Middle Distillate",
                    "Jet Fuel", "Gas Oil", " Diesel", "Condensate", "Fuel Oil and Bunker", "Brent", "WTI",
                    "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil", "Gasoil", "Marine gasoil",
                    "Far east index", "propane", "butane", "Mt Belv Propane", "Mt Belv Butane", "ULSD New york",
                    "UlSD"],
    "Trade and Export": ["trading", "export", "import", "oil exports", "oil imports",],

}

nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

class SophisticatedKeywordGeneratorTool(BaseTool):
    name: str = "SophisticatedKeywordGeneratorTool"
    description: str = "This tool generates specific keywords from a given high-level topic using advanced NLP techniques."

    def _run(self, topic: str) -> list:
        # Use spaCy to process the text
        doc = nlp(topic)

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
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text.lower() not in STOP_WORDS and ('oil' in chunk.text.lower() or 'gas' in chunk.text.lower())]
        print("noun chunks extracted ", noun_chunks)
        # Use RAKE to extract keywords
        rake = Rake()
        rake.extract_keywords_from_text(topic)
        rake_keywords = rake.get_ranked_phrases()
        print("rake keywords extracted ", rake_keywords)
        # Combine all keywords
        all_keywords = entities + noun_chunks + rake_keywords
        print("all keywords extracted", all_keywords)
        specific_keywords = [
            "oil-prices", "gas-prices", "oil-stock-market", "oil-company",
            "oil-supply", "oil-demand", "oil-production", "gas-production",
            "energy-market", "oil-trading", "gas-trading", "crude-oil",
            "natural-gas", "commodity-prices", "oil-futures", "gas-futures",
            "exploration", "refining", "pipelines", "oilfield-services",
            "petroleum", "downstream", "upstream", "midstream", "LNG",
            "oil-reserves", "drilling", "shale-oil",
            "oil-exports", "oil-imports", "OPEC",
            "oil-consumption", "oil-inventory",
            "Light-Distillate", "Naphtha", "Gasoline", "LPG", " Biofuels", "Middle-Distillate",
            "Jet-Fuel", "Gas-Oil", "Diesel", "Condensate", "Fuel-Oil-and-Bunker", "Brent", "WTI",
            "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe-Gasoil", "Gasoil", "Marine-gasoil",
            "Far-east-index", "propane", "butane", "Mt-Belv-Propane", "Mt-Belv-Butane", "ULSD-New-York",
            "UlSD"
        ]
        # Add domain-specific keywords

        print(len(specific_keywords))
        all_keywords += specific_keywords
        print("total keywords ", all_keywords)
        print(len(all_keywords))
        # Deduplicate and filter keywords
        keywords = list(set(all_keywords))
        print("keywords filtered ", keywords)
        print(len(keywords))
        # Refine keywords to avoid unrelated topics
        refined_keywords = [kw for kw in keywords if 'stock' not in kw or 'oil' in kw or 'gas' in kw]
        print("keywords refined : ", refined_keywords)
        print(len(refined_keywords))
        return refined_keywords

def fetch_rss(rss_url, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(rss_url)
            if response.status_code == 429:
                print(f"Rate limit exceeded for {rss_url}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Use time.sleep for a blocking delay
                continue
            if response.status_code != 200:
                print(f"Failed to fetch {rss_url}: Status {response.status_code}")
                return None
            return response.text
        except Exception as e:
            print(f"Error fetching {rss_url}: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return None

def fetch_rss_entries(refined_keyword):
    rss_url = f"https://www.bing.com/news/search?q={refined_keyword}&format=rss"
    print(f"Fetching RSS URL: {rss_url}")

    rss_feed = fetch_rss(rss_url)
    if rss_feed is None:
        print(f"Failed to fetch content for URL: {rss_url}")
        return []

    print(f"Fetched content for URL: {rss_url}")

    feed = feedparser.parse(rss_feed)
    if not feed.entries:
        print(f"No entries found in feed for keyword: {refined_keyword}")
        return []

    three_days_ago = datetime.now() - timedelta(days=3)
    entries = [
        {
            "Title": entry.title,
            "Link": entry.link,
            "Published": entry.published
        }
        for entry in feed.entries
        if datetime(*entry.published_parsed[:6]) >= three_days_ago
    ]

    if not entries:
        print(f"No recent entries found for keyword: {refined_keyword}")
    else:
        print(f"Found {len(entries)} entries for keyword: {refined_keyword}")

    return entries

def run_tasks(refined_keywords):
    articles = []
    for keyword in refined_keywords:
        articles.extend(fetch_rss_entries(keyword))
    return articles

class RSSFeedScraperTool(BaseTool):
    name: str = "RSSFeedScraperTool"
    description: str = ("This tool dynamically generates RSS feed URLs from keywords and "
                        "scrapes them to extract news articles. It returns a list of "
                        "articles with titles and links from the past week.")

    def _run(self, refined_keywords: list) -> list:
        articles = run_tasks(refined_keywords)

        if not articles:
            print("No articles found after scraping.")

        print(articles)
        return articles

def is_accessible(url, retries=3, backoff_factor=0.5):
    for attempt in range(retries):
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code == 200:
                return True
            if response.status_code in [401, 403, 404]:  # Unauthorized, Forbidden, Not Found
                return False
            if "login" in str(response.url) or "subscribe" in str(response.url):
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error checking URL {url}: {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))
                continue
    return False

def score_relevancy(article, relevant_keywords):
    title = article["Title"].lower()
    content = article.get("Content", "").lower()  # Assuming article content is also available
    score = 0

    for keyword in relevant_keywords:
        if keyword in title:
            score += 2  # Higher weight for keywords in title
        if keyword in content:
            score += 1

    print(f"Article: {title}, Relevancy Score: {score}")
    return score

def is_similar(title1, title2, threshold=0.7):
    similarity_ratio = SequenceMatcher(None, title1, title2).ratio()
    print(f"Comparing: {title1} with {title2}, Similarity Ratio: {similarity_ratio}")
    return similarity_ratio > threshold

def group_articles_by_category(articles):
    categorized_articles = defaultdict(list)

    for article in articles:
        for category in article["Categories"]:
            categorized_articles[category].append(article)

    return categorized_articles

def categorize_article(article, categories):
    title = article["Title"].lower()
    content = article.get("Content", "").lower()  # Assuming article content is also available
    article_categories = []

    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords) or any(keyword in content for keyword in keywords):
            article_categories.append(category)

    return article_categories

def create_unique_key(article):
    return (
        normalize_title(article["Title"]),
        article["Link"],
        article.get("Published"),
        tuple(article.get("Categories", []))
    )

def normalize_title(title):
    # Convert to lowercase and remove non-alphanumeric characters
    return re.sub(r'\W+', '', title.lower())

def filter_articles(article_chunks, relevant_keywords, categories, relevancy_threshold):
    unique_articles = set()
    filtered_articles = []

    for chunk in article_chunks:
        for article in chunk:
            unique_key = create_unique_key(article)

            # Check for exact duplicates using the unique key
            if unique_key in unique_articles:
                continue

            # Adding unique_key to the set
            unique_articles.add(unique_key)

            # Calculate relevancy score
            relevancy_score = score_relevancy(article, relevant_keywords)
            if relevancy_score < relevancy_threshold:
                continue

            # Check if the article is accessible
            if not is_accessible(article["Link"]):
                continue

            # Check for similarity
            is_duplicate = any(is_similar(normalize_title(article["Title"]), seen_key[0], 0.6) for seen_key in unique_articles)
            if is_duplicate:
                continue

            article_categories = categorize_article(article, categories)
            filtered_articles.append({
                "Title": article["Title"],
                "Link": article["Link"],
                "Published": article.get("Published"),
                "Categories": article_categories
            })

    print(f"Filtered Articles: {filtered_articles}")
    return filtered_articles

def filter_and_categorize_articles(all_articles_output):
    # Load articles from JSON file
    with open(all_articles_output, 'r') as f:
        articles = json.load(f)

    # Split articles into chunks
    chunk_size = max(1, len(articles) // 2)  # Adjust chunk size as needed
    article_chunks = [articles[i:i + chunk_size] for i in range(0, len(articles), chunk_size)]

    # Filter articles for redundancy, relevancy, and categorize them
    filtered_articles = filter_articles(article_chunks, relevant_keywords, categories, relevancy_threshold=2)
    print("Articles have been filtered", filtered_articles)

    # Group articles by category
    grouped_articles = group_articles_by_category(filtered_articles)
    print("Articles have been grouped", grouped_articles)

    # Save each category's articles to separate JSON files
    category_output_dir = './reports/categorized_news_reports'
    os.makedirs(category_output_dir, exist_ok=True)

    for category, articles in grouped_articles.items():
        category_file = os.path.join(category_output_dir, f'{category.replace(" ", "_").lower()}_news_report.json')
        with open(category_file, 'w') as f:
            json.dump(articles, f, indent=2)
        print(f"{category} articles saved into {category_file}")

# Generate keywords
keywords = SophisticatedKeywordGeneratorTool()._run(topic)

# Fetch RSS feeds
result = RSSFeedScraperTool()._run(keywords)

# Save the articles to JSON, and filter and categorize them
all_articles_output = "C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/reports/news_report.json"
with open(all_articles_output, 'w') as f:
    json.dump(result, f, indent=2)

print("Stage 1 : articles saved into json file")

filter_and_categorize_articles(all_articles_output)