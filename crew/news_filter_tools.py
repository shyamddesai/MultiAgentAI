import json
import os
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime, timedelta
from MultiAgentAI.crew.config import relevant_keywords, categories, general_keywords


def filter_and_categorize_articles(all_articles_output):
    # Load articles from JSON file
    with open(all_articles_output, 'r') as f:
        articles = json.load(f)

    # Filter articles for redundancy, relevancy, and categorize them
    filtered_articles = filter_articles(articles, relevant_keywords, categories, relevancy_threshold=1.5)
    print("Filtered articles: ", filtered_articles)

    filtered_output = "./reports/filtered_news_report.json"
    with open(filtered_output, 'w') as f:
        json.dump(filtered_articles, f, indent=2)

    # # Group articles by category
    # grouped_articles = group_articles_by_category(filtered_articles)
    # print("articles are grouped")
    # # Save each category's articles to separate JSON files
    # category_output_dir = './reports/categorized_news_reports'
    # os.makedirs(category_output_dir, exist_ok=True)
    #
    # for category, articles in grouped_articles.items():
    #     category_file = os.path.join(category_output_dir, f'{category.replace(" ", "_").lower()}_news_report.json')
    #     with open(category_file, 'w') as f:
    #         json.dump(articles, f, indent=2)
    #
    # print(f"All articles are filtered and categorized in '{category_output_dir}'")

    return filtered_articles # Comment out if you want to group articles by category

# ------------------------------------------------------------------------------

def group_articles_by_category(articles):
    categorized_articles = defaultdict(list)

    for article in articles:
        for category in article["Categories"]:
            categorized_articles[category].append(article)
        print("Categorizing:", article)
    return categorized_articles

# ------------------------------------------------------------------------------

# def is_accessible(url, retries=3, backoff_factor=0.5):
#     for attempt in range(retries):
#         try:
#             response = requests.head(url, allow_redirects=True)
#             if response.status_code == 200:
#                 return True
#             if response.status_code in [401, 403, 404]:  # Unauthorized, Forbidden, Not Found
#                 return False
#             if "login" in response.url or "subscribe" in response.url:
#                 return False
#         except requests.ConnectionError:
#             if attempt < retries - 1:
#                 time.sleep(backoff_factor * (2 ** attempt))
#                 continue
#         except Exception as e:
#             print(f"Error checking URL {url}: {e}")
#             return False
#     return False

# ------------------------------------------------------------------------------

def is_similar(title1, title2, threshold=0.6):
    return SequenceMatcher(None, title1, title2).ratio() > threshold

# ------------------------------------------------------------------------------

def score_relevancy(article, relevant_keywords):
    title = article["Title"].lower()
    score = 0

    for keyword in relevant_keywords:
        if keyword in title:
            score += 2  # Higher weight for keywords in title
    for keyword in general_keywords:
        if keyword in title:
            score += 0.5
    return score

# ------------------------------------------------------------------------------

def categorize_article(article, categories):
    title = article["Title"].lower()
    article_categories = []

    for category, keywords in categories.items():
        if any(keyword in title for keyword in keywords):
            article_categories.append(category)

    return article_categories

# ------------------------------------------------------------------------------

def filter_articles(articles, relevant_keywords, categories, relevancy_threshold=1.5):
    unique_titles = set()
    unique_urls = set()
    filtered_articles = []

    for article in articles:
        title = article["Title"]
        url = article["Link"]
        published = article.get("Published")

        # Skip articles with duplicate titles or URLs
        if title in unique_titles or url in unique_urls:
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

        # Assume all URLs are accessible, remove the is_accessible call
        unique_titles.add(title)
        unique_urls.add(url)
        article_categories = categorize_article(article, categories)
        filtered_articles.append({
            "Title": title,
            "Link": url,
            "Published": published,
            "Categories": article_categories
        })

    return filtered_articles
