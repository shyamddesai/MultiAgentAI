import json
import os

def filter_articles_by_keywords_in_title_or_content(selected_keywords):
    # Path to the original JSON file
    input_file_path = './reports/temp/temp_filtered_news_report.json'

    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"File not found: {input_file_path}")
        return []

    print(f"Loading file: {input_file_path}")

    # Load the original JSON file
    with open(input_file_path, 'r') as file:
        articles = json.load(file)

    # Print the number of articles loaded
    print(f"Number of articles loaded: {len(articles)}")

    # List to hold filtered articles
    filtered_articles = []

    for article in articles:
        title = article.get('Title', '')
        content = article.get('Content', '')

        if title:
            title = title.lower()
        else:
            title = ''

        if content:
            content = content.lower()
        else:
            content = ''

        if any(keyword.lower() in title or keyword.lower() in content for keyword in selected_keywords):
            filtered_articles.append(article)

    # Print the number of filtered articles
    print(f"Number of filtered articles: {len(filtered_articles)}")

    return filtered_articles

def cherry_picking(selected_keywords):
    # Filter the articles
    filtered_articles = filter_articles_by_keywords_in_title_or_content(selected_keywords)

    # Check if any articles were filtered
    if filtered_articles:
        # Ensure the directory exists
        output_dir = os.path.join(os.getcwd(), './reports')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the filtered articles to a new JSON file
        filtered_file_path = os.path.join(output_dir, 'FINAL_Filter_by_keywords.json')
        print(f"Saving filtered articles to: {filtered_file_path}")

        with open(filtered_file_path, 'w') as filtered_file:
            json.dump(filtered_articles, filtered_file, indent=2)

        print("Filtered articles saved successfully.")
    else:
        print("No articles matched the keywords.")
        return 1
