import json
import os


# Function to filter articles by keywords in the title
# Function to filter articles by keywords in the title or content
def filter_articles_by_keywords_in_title_or_content():
    # Load the original JSON file
    with open('C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/reports/processed_articles/cleaned_exploration_news_report.json',
                           'r') as file:
        articles = json.load(file)

    # Keywords to filter by
    keywords = ["Natural Gas", "Oil"]

    filtered_articles = []
    for article in articles:
        title = article.get('Title', '').lower()
        content = article.get('Content', '').lower()
        if any(keyword in title or keyword in content for keyword in keywords):
            filtered_articles.append(article)
    return filtered_articles


# Filter the articles
filtered_articles = filter_articles_by_keywords_in_title_or_content()





