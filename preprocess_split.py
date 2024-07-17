import json
import os

def split_title(s):
    idx = s.rfind('-')

    if idx != -1:
        return s[:idx], s[idx+1:]
    else:
        return s, ''

def split_articles(json_file):
    category = os.path.splitext(os.path.basename(json_file))[0].replace('cleaned_', '').replace('_news_report', '')
    with open(json_file, 'r') as file:
        data = json.load(file)

    output_dir = f'./reports/processed_articles/{category}/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 

    for index, entry in enumerate(data):
        content = entry.get('Content')
        if content is not None:
            old_title = entry.get('Title')
            title, source = split_title(old_title)
            output = {}
            output['title'] = title
            output['source'] = source
            output['Content'] = content
            with open(output_dir + f'content_{index}.json', 'w') as outfile:
                json.dump(output, outfile, indent=4)
        else:
            print(f"Warning: No 'content' key found in entry {index}")
def split(category):
    with open(f'./reports/processed_articles/cleaned_{category}_news_report.json', 'r') as file:
        data = json.load(file)

    output_dir = f'./reports/processed_articles/{category}/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) 

    for index, entry in enumerate(data):
        output_data = {}
        if 'Content' in entry:
            output_data['title'], output_data['source'] = split_title(entry['Title'])
            output_data['Content'] = entry['Content']
            
        else:
            print(f"Warning: No 'Content' key found in entry {index}")
        
        if output_data:
            with open(output_dir+f'entry_{index}.json', 'w') as outfile:
                json.dump(output_data, outfile, indent=4)

split('exploration')
