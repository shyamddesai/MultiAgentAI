import json

def txt_to_json(txt_file_path, json_file_path):
    with open(txt_file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    articles = []
    current_article = {}
    for line in lines:
        line = line.strip()
        if not line:
            if current_article:
                articles.append(current_article)
                current_article = {}
        else:
            if ': ' in line:
                key, value = line.split(': ', 1)
                current_article[key] = value

    # Add the last article if it exists
    if current_article:
        articles.append(current_article)

    with open(json_file_path, 'w') as json_file:
        json.dump(articles, json_file, indent=2)


# Specify the file paths
txt_file_path = '../crew/news_rank.txt'
json_file_path = '../crew/news_rank.json'

# Convert TXT to JSON
txt_to_json(txt_file_path, json_file_path)

print(f"Converted {txt_file_path} to {json_file_path}")
