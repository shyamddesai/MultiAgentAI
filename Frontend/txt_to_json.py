import json
import re

def parse_article(article_text):
    # Extract title
    title_match = re.search(r'### Article \d+: "(.*?)"', article_text)
    title = title_match.group(1) if title_match else "Unknown Title"

    # Extract source and source URL
    source_match = re.search(r'Source: \[(.*?)\]\((.*?)\)', article_text)
    source = source_match.group(1) if source_match else "Unknown Source"
    source_url = source_match.group(2) if source_match else "Unknown URL"

    # Extract date
    date_match = re.search(r'Published: (.*?)\n', article_text)
    date = date_match.group(1) if date_match else "Unknown Date"

    # Extract content
    content_match = re.search(r'Published: .*?\n\n(.*)', article_text, re.DOTALL)
    content = content_match.group(1).strip() if content_match else "No Content"

    return {
        "Title": title,
        "Source": source,
        "Date": date,
        "Content": content
    }, {
        "Source": source,
        "Address": source_url
    }

def convert_to_json(input_filename, output_article_filename, output_source_filename):
    with open(input_filename, 'r') as file:
        text = file.read()

    # Split the text into articles
    articles = text.split('### Article ')[1:]  # Skip the first part before the first article

    # Parse each article
    parsed_articles = []
    parsed_sources = []
    for article in articles:
        article_data, source_data = parse_article('### Article ' + article)
        parsed_articles.append(article_data)
        parsed_sources.append(source_data)

    # Write articles to JSON file
    with open(output_article_filename, 'w') as json_file:
        json.dump(parsed_articles, json_file, indent=4)

    # Write sources to JSON file
    with open(output_source_filename, 'w') as json_file:
        json.dump(parsed_sources, json_file, indent=4)

if __name__ == '__main__':
    input_filename = 'news_report_analysis.txt'
    output_article_filename = '1.json'
    output_source_filename = '2.json'
    convert_to_json(input_filename, output_article_filename, output_source_filename)
    print(f"Converted {input_filename} to {output_article_filename} and {output_source_filename}")