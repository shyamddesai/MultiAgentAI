import os
import json
import random

# Directory containing the JSON files
market_analysis_dir = 'data/sample_marketAnalysis'

# Function to generate mock data
def generate_mock_data():
    return {
        "Current Price": round(random.uniform(50, 150), 2),
        "Moving Average": round(random.uniform(50, 150), 2),
        "Trend": random.choice(["Bearish", "Bullish"])
    }

# Iterate over each file in the directory
for filename in os.listdir(market_analysis_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(market_analysis_dir, filename)
        
        # Empty the file
        with open(file_path, 'w') as file:
            file.write('{}')
        
        # Read the existing data (which is now empty)
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Add mock data
        data['Data'] = generate_mock_data()
        
        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

print("Mock data added to all JSON files in the @marketAnalysis directory.")