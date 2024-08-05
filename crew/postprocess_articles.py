import json

def remove_duplicates_and_null_content(articles):
    seen_titles = set()
    seen_published_dates = set()
    unique_articles = []

    for article in articles:
        title = article.get('Title')
        published_date = article.get('Published')
        content = article.get('Content')
        
        # Skip if the title, published date is a duplicate, or content is null
        if title in seen_titles or published_date in seen_published_dates or content is None or content == "":
            continue
        
        seen_titles.add(title)
        seen_published_dates.add(published_date)
        unique_articles.append(article)

    return unique_articles

def process_json_file(input_file, output_file):
    with open(input_file, 'r') as file:
        articles = json.load(file)
    
    unique_articles = remove_duplicates_and_null_content(articles)
    
    with open(output_file, 'w') as file:
        json.dump(unique_articles, file, indent=2)
