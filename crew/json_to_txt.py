import json

def json_to_txt(json_file_path, txt_file_path):
    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Open the TXT file for writing
    with open(txt_file_path, 'w') as txt_file:
        # Check if data is a list
        if isinstance(data, list):
            # Iterate over each item in the JSON data
            for item in data:
                # Check if the item is a dictionary
                if isinstance(item, dict):
                    # Write each key-value pair to the TXT file
                    for key, value in item.items():
                        txt_file.write(f"{key}: {value}\n")
                    txt_file.write("\n")  # Add a newline for separation between items
                else:
                    txt_file.write(f"Non-dictionary item: {item}\n")
                    txt_file.write("\n")
        else:
            txt_file.write(f"Expected a list, but got: {type(data)}\n")
            txt_file.write(f"Data: {data}\n")


# Specify the file paths
json_file_path = 'C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/crew/news_rank.json'
txt_file_path = '/MultiAgentAI/reports/news_rank_goldenModel.txt'

# Convert JSON to TXT
json_to_txt(json_file_path, txt_file_path)

print(f"Converted {json_file_path} to {txt_file_path}")
