import json
import os


def filter_articles_by_keywords_in_title_or_content():
    # Path to the original JSON file
    input_file_path = '../reports/processed_articles/cleaned_exploration_news_report.json'

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"File not found: {input_file_path}")
        return {}

    print(f"Loading file: {input_file_path}")

    # Load the original JSON file
    with open(input_file_path, 'r') as file:
        articles = json.load(file)

    # Print the number of articles loaded
    print(f"Number of articles loaded: {len(articles)}")

    # Keywords to filter by
    keywords = ["WTI", "crude oil", "usa", "forecast"]

    # Dictionary to hold filtered articles categorized by keyword
    categorized_articles = {keyword: [] for keyword in keywords}

    for article in articles:
        title = article.get('Title', '').lower()
        content = article.get('Content', '').lower()
        for keyword in keywords:
             if keyword.lower() in title or keyword.lower() in content:
            # if keyword.lower() in content:
                categorized_articles[keyword].append(article)
                break  # Assumes each article should be categorized under only one keyword

    # Print the number of filtered articles for each keyword
    for keyword, articles in categorized_articles.items():
        print(f"Number of articles for keyword '{keyword}': {len(articles)}")

    return categorized_articles


# Filter the articles
categorized_articles = filter_articles_by_keywords_in_title_or_content()

# Save the filtered articles to a new JSON file
filtered_file_path = os.path.join(os.getcwd(), '../reports/FINAL_Filter_by_keywords.json')
print(f"Saving filtered articles to: {filtered_file_path}")

with open(filtered_file_path, 'w') as filtered_file:
    json.dump(categorized_articles, filtered_file, indent=2)

print("Filtered articles saved successfully.")
