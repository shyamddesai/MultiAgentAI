import json
import os


def split(category):
    with open(f'./reports/processed_articles/cleaned_{category}_news_report.json', 'r') as file:
        data = json.load(file)

    output_dir = f'./reports/processed_articles/{category}/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 

    for index, entry in enumerate(data):
        output_data = {}
        if 'Content' in entry:
            output_data['Content'] = entry['Content']
        else:
            print(f"Warning: No 'Content' key found in entry {index}")

        if 'Title' in entry:
            output_data['Title'] = entry['Title']
        else:
            print(f"Warning: No 'Title' key found in entry {index}")
        
        if output_data:
            with open(output_dir+f'entry_{index}.json', 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

split('exploration')
