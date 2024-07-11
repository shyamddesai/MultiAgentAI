import os
import requests
from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer
import json

# Configuration for HTML Sanitizer
sanitizer = Sanitizer({
    'tags': ('b', 'blockquote', 'code', 'dd', 'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'i', 'li', 'ol', 'p', 'pre', 's', 'strike', 'strong', 'sub', 'sup', 'u', 'ul'),
    'attributes': {},
    'empty': set(),  # Tags allowed to be empty (excluding 'iframe', 'video', 'audio', 'object', 'embed')
    'separate': ('p', 'li', 'div'),
    'whitespace': {'pre', 'code'},  # Tags where whitespace should be maintained
    'keep_nested_blockquote': True,
})

def scrape_and_clean(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        before_length = len(html_content)
        
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Optionally remove unwanted elements (like scripts and styles)
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get the cleaned HTML
        cleaned_html = sanitizer.sanitize(str(soup))
        after_length = len(cleaned_html)
        
        return cleaned_html, before_length, after_length
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None, 0, 0

# Example usage with the provided JSON file
def process_articles(category):
    json_file = './reports/categorized_news_reports/{}_news_report.json'.format(category)
    with open(json_file, 'r') as file:
        articles = json.load(file)
    
    for article in articles:
        if "cleaned_content" in article:
            url = article['Link']
            cleaned_content, before_length, after_length = scrape_and_clean(url)
            if cleaned_content:
                article['CleanedContent'] = cleaned_content
                print(f"Successfully cleaned content for {url}")
                print(f"Before: {before_length} characters, After: {after_length} characters, Reduced by: {before_length - after_length} characters")
                output_dir = './reports/categorized_news_reports/{}/'.format(category)
                output_file = output_dir+article['Title']
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                if not os.path.exists(output_file):
                    with open(output_file, 'w') as file:
                        file.write('')
                with open(output_file, 'w') as file:        
                    json.dump(article, file, indent=2)
            else:
                article['CleanedContent'] = None
                print(f"Failed to clean content for {url}")
        
        else:
            output_dir = './reports/categorized_news_reports/{}/'.format(category)
            output_file = output_dir+article['Title']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            if not os.path.exists(output_file):
                with open(output_file, 'w') as file:
                    file.write('')
            with open(output_file, 'w') as file:        
                json.dump(article, file, indent=2)
    
    # Ensure the directory exists
    # output_file = 'cleaned_' + json_file
    # output_dir = os.path.dirname(output_file)
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)
    
    # # Create the file if it doesn't exist
    # if not os.path.exists(output_file):
    #     with open(output_file, 'w') as file:
    #         file.write('')
    
    # # Save the updated articles to the JSON file
    # with open(output_file, 'w') as file:
    #     json.dump(articles, file, indent=2)

# Execution
categories = ['company_news', 'exploration', 'market_trends', 'production_updates', 'refining', 'stock_prices', 'supply_and_demand', 'trade_and_export']
# for category in categories:
#     process_articles(category)
process_articles('cleaned_exploration')
