import json
import os
import aiohttp
import asyncio
from collections import defaultdict
from difflib import SequenceMatcher
from MultiAgentAI.crew.config import relevant_keywords, categories

def filter_and_categorize_articles(all_articles_output):
    # Load articles from JSON file
    with open(all_articles_output, 'r') as f:
        articles = json.load(f)

    # Filter articles for redundancy, relevancy, and categorize them
    filtered_articles = asyncio.run(filter_articles_async(articles, relevant_keywords, categories, relevancy_threshold=3))

    filtered_output = "./reports/filtered_news_report.json"
    with open(filtered_output, 'w') as f:
        json.dump(filtered_articles, f, indent=2)

    # Group articles by category
    grouped_articles = group_articles_by_category(filtered_articles)

    # Save each category's articles to separate JSON files
    category_output_dir = './reports/categorized_news_reports'
    os.makedirs(category_output_dir, exist_ok=True)

    for category, articles in grouped_articles.items():
        category_file = os.path.join(category_output_dir, f'{category.replace(" ", "_").lower()}_news_report.json')
        with open(category_file, 'w') as f:
            json.dump(articles, f, indent=2)

    print(f"All articles are filtered and categorized in '{category_output_dir}'")

# ------------------------------------------------------------------------------

def group_articles_by_category(articles):
    categorized_articles = defaultdict(list)

    for article in articles:
        for category in article["Categories"]:
            categorized_articles[category].append(article)

    return categorized_articles

# ------------------------------------------------------------------------------

async def is_accessible(session, url, retries=3, backoff_factor=0.5):
    for attempt in range(retries):
        try:
            async with session.head(url, allow_redirects=True) as response:
                if response.status == 200:
                    return True
                if response.status in [401, 403, 404]:  # Unauthorized, Forbidden, Not Found
                    return False
                if "login" in str(response.url) or "subscribe" in str(response.url):
                    return False
        except aiohttp.ClientConnectionError:
            if attempt < retries - 1:
                await asyncio.sleep(backoff_factor * (2 ** attempt))
                continue
        except Exception as e:
            print(f"Error checking URL {url}: {e}")
            return False
    return False

# ------------------------------------------------------------------------------

def is_similar(title1, title2, threshold=0.7):
    return SequenceMatcher(None, title1, title2).ratio() > threshold

# ------------------------------------------------------------------------------

def score_relevancy(article, relevant_keywords):
    title = article["Title"].lower()
    content = article.get("Content", "").lower()  # Assuming article content is also available
    score = 0

    for keyword in relevant_keywords:
        if keyword in title:
            score += 2  # Higher weight for keywords in title
        if keyword in content:
            score += 1

    return score

# ------------------------------------------------------------------------------

def categorize_article(article, categories):
    title = article["Title"].lower()
    content = article.get("Content", "").lower()  # Assuming article content is also available
    article_categories = []

    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords) or any(keyword in content for keyword in keywords):
            article_categories.append(category)

    return article_categories

# ------------------------------------------------------------------------------

async def filter_articles_async(articles, relevant_keywords, categories, relevancy_threshold=3):
    unique_titles = set()
    filtered_articles = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for article in articles:
            title = article["Title"]
            url = article["Link"]
            published = article.get("Published")

            if title in unique_titles:
                continue

            is_duplicate = False
            for seen_title in unique_titles:
                if is_similar(title, seen_title):
                    is_duplicate = True
                    break

            if is_duplicate:
                continue

            relevancy_score = score_relevancy(article, relevant_keywords)
            if relevancy_score < relevancy_threshold:
                continue

            tasks.append((article, asyncio.create_task(is_accessible(session, url))))

        results = await asyncio.gather(*[task for _, task in tasks])

        for (article, task) in zip(tasks, results):
            if task:
                title = article[0]["Title"]
                url = article[0]["Link"]
                published = article[0].get("Published")
                unique_titles.add(title)
                article_categories = categorize_article(article[0], categories)
                filtered_articles.append({
                    "Title": title,
                    "Link": url,
                    "Published": published,
                    "Categories": article_categories
                })

    return filtered_articles