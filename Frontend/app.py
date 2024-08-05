from quart import Quart, render_template, request, redirect, session, url_for, Response, jsonify
from datetime import datetime
import orjson
import aiofiles
import os
import json

app = Quart(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)
app.secret_key = 'supersecretkey'  # Needed for session management

# Determine the root directory of the project dynamically
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.after_request
async def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
async def home():
    return await render_template('uimock_flash.html')

@app.route('/static_page')
async def static_page():
    return await render_template('static_page.html')

@app.route('/loading')
async def loading():
    return redirect(url_for('feed'))

@app.route('/feed')
async def feed():
    current_date = datetime.now().strftime("%d %B")
    keywords = session.get('keywords', [])
    market_analysis_dir = os.path.join(project_root, 'Data/marketAnalysis')
    market_data = []

    for subdir in os.listdir(market_analysis_dir):
        subdir_path = os.path.join(market_analysis_dir, subdir)
        if os.path.isdir(subdir_path):
            report_path = os.path.join(subdir_path, 'market.json')
            if os.path.exists(report_path):
                async with aiofiles.open(report_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.loads(await file.read())
                        if isinstance(data, list) and len(data) > 0:
                            # Convert trend list to a string
                            data[0]['trend'] = ', '.join(data[0]['trend']) if 'trend' in data[0] else 'N/A'
                            market_data.append({
                                "filename": subdir,
                                "data": data[0]  # Assuming we want the first object in the array
                            })
                    except json.JSONDecodeError:
                        market_data.append({
                            "filename": subdir,
                            "data": {"commodity": "N/A", "currentPrice": "N/A", "movingAverage": "N/A", "trend": "N/A"}
                        })
                    
    print(market_data)
    return await render_template('feed.html', keywords=keywords, current_date=current_date, market_data=market_data)

specific_keywords = [
    "Oil Prices", "Gas Prices", "Oil and Gas Stock Market", "Exploration", "Refining", "Pipelines", "Oilfield Services", "Petroleum", "Downstream", "Upstream", "Midstream",
    "LNG", "Reserves", "Drilling", "Shale oil", "Offshore Drilling", "Exports", "Imports", "OPEC", "Refining Capacity", "Production Cuts", "Consumption", "Inventory",
    "Crude Oil", "Natural Gas", "Petrol", "Diesel", "Jet Fuel", "Gasoline"
]

@app.route('/suggest_keywords')
async def suggest_keywords():
    return Response(orjson.dumps(specific_keywords), mimetype='application/json')


@app.route('/split-screen2')
async def split_screen2():
    async with aiofiles.open(os.path.join(project_root, 'Data/reports/reports/highlights.json'), 'r', encoding='utf-8') as highlights_file:
        highlights_data = orjson.loads(await highlights_file.read())
        
    async with aiofiles.open(os.path.join(project_root, 'Data/reports/reports/report.json'), 'r', encoding='utf-8') as report_file:
        report_data = orjson.loads(await report_file.read())
        
    async with aiofiles.open(os.path.join(project_root, 'Data/reports/sources/sources_sentiment.json'), 'r', encoding='utf-8') as sources_file:
        sources_data = orjson.loads(await sources_file.read())
    
    return await render_template('split_screen2.html', highlights_data=highlights_data, report_data=report_data, sources_data=sources_data)

@app.route('/process_next', methods=['POST'])
async def process_next():
    data = await request.json
    keywords = data.get('keywords', '')
    selected_words = data.get('selectedWords', '')
    
    print(f"Keywords: {keywords}")
    print(f"Selected Words: {selected_words}")
    
    async with aiofiles.open(os.path.join(project_root, 'Frontend/data/userInput/selected_keywords.txt'), 'w') as file:
        await file.write(f"{keywords}\n\n")
        
    async with aiofiles.open(os.path.join(project_root, 'Frontend/data/userInput/selected_commodities.txt'), 'w') as file:
        await file.write('\n'.join(selected_words.split(',')) + '\n')
    
    session['selected_categories'] = selected_words.split(',')
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)