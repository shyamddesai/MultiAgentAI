import os
import requests
import json
import re
from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuration for HTML Sanitizer
sanitizer = Sanitizer({
    'tags': {'b', 'blockquote', 'code', 'dd', 'div', 'dl', 'dt', 'em', 'h1', 'h2', 'h3', 'i', 'ol', 'pre', 's', 'strike', 'strong', 'sub', 'sup', 'u'},
    'attributes': {},
    'empty': set(),
    'separate': {'div'},
    'whitespace': {'pre', 'code'},
    'keep_nested_blockquote': True,
})

# Replace unicode characters for better readability and to reduce character count
def replace_unicode_characters(text):
    unicode_replacements = {
        '\u2010': '-', '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u00a9': '(c)', '\u00ae': '(r)', '\u2026': '...', '\u00b0': ' degrees', '\u00a3': '£', '\u20ac': '€',
        '\u00a5': '¥', '\u00a2': '¢', '\u2022': '*', '\u00a0': ' ', '\u00b7': '·', '\u00e9': 'e', '\u2715': 'x',
        '\n': ' ', '\u0095': '*', '\"': '"', '\u00bb': '>>', '\u00d7': 'x'
    }
    for unicode_char, replacement in unicode_replacements.items():
        text = text.replace(unicode_char, replacement)
    return text

def remove_headers_footers(soup):
    # Remove common header/footer elements
    header_tags = ['header', 'nav', 'aside', 'footer']
    footer_patterns = ['Subscribe', 'Copyright', 'Legalities', 'Contact Us']

    for tag in header_tags:
        for element in soup.find_all(tag):
            element.extract()
    
    for pattern in footer_patterns:
        for element in soup.find_all(text=re.compile(pattern)):
            element.extract()
    
    return soup

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
        
        # Remove common headers and footers
        soup = remove_headers_footers(soup)
        
        # Get the cleaned HTML
        cleaned_html = sanitizer.sanitize(str(soup))
        
        # Remove unnecessary tags and get text content
        soup_cleaned = BeautifulSoup(cleaned_html, 'html.parser')
        text_content = soup_cleaned.get_text(separator='\n')
        after_length = len(text_content)

        # Replace Unicode characters with ASCII equivalents
        text_content = replace_unicode_characters(text_content)
        
        return text_content, before_length, after_length
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return scrape_and_clean_with_selenium(url)
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return None, 0, 0

def scrape_and_clean_with_selenium(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        html_content = driver.page_source
        before_length = len(html_content)

        soup = BeautifulSoup(html_content, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        
        soup = remove_headers_footers(soup)
        
        cleaned_html = sanitizer.sanitize(str(soup))
        
        soup_cleaned = BeautifulSoup(cleaned_html, 'html.parser')
        text_content = soup_cleaned.get_text(separator='\n')
        after_length = len(text_content)
        
        text_content = replace_unicode_characters(text_content)
        
        driver.quit()
        print(f"Successfully scraped content for {url} using Selenium")
        return text_content, before_length, after_length
    except Exception as e:
        print(f"Selenium error for {url}: {e}")
        return None, 0, 0

def process_articles(json_file):
    with open(json_file, 'r') as file:
        articles = json.load(file)
    
    for article in articles:
        url = article['Link']
        cleaned_content, before_length, after_length = scrape_and_clean(url)
        if cleaned_content:
            article['Content'] = cleaned_content
            reduction_percentage = ((before_length - after_length) / before_length) * 100
            print(f"Successfully cleaned content for {url}")
            print(f"Before: {before_length} characters, After: {after_length} characters, Reduced by: {before_length - after_length} characters ({reduction_percentage:.2f}%)")
        else:
            article['Content'] = None
            print(f"Failed to clean content for {url}")
    
    # Ensure the directory exists
    output_dir = './reports/processed_articles'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set the output file path
    output_file = os.path.join(output_dir, 'cleaned_' + os.path.basename(json_file))
    failed_file = os.path.join(output_dir, 'failed_' + os.path.basename(json_file))

    # Save failed articles to a separate JSON file
    failed_articles = [a for a in articles if not a['Content']]
    if failed_articles:
        with open(failed_file, 'w') as file:
            json.dump(failed_articles, file, indent=2)
    else:
        if os.path.exists(failed_file):
            os.remove(failed_file)

    # Save failed articles to a separate JSON file
    with open(failed_file, 'w') as file:
        json.dump([a for a in articles if not a['Content']], file, indent=2)

# ------------------------------------------------------------------------------

def process_all_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            print(f"\n\nProcessing file: {file_path}")
            process_articles(file_path)

process_all_json_files('./reports/categorized_news_reports')