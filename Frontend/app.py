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

async def load_json_data(file_path):
    try:
        async with aiofiles.open(file_path, 'r') as file:
            return orjson.loads(await file.read())
    except (FileNotFoundError, orjson.JSONDecodeError) as e:
        app.logger.error(f"Error loading JSON from {file_path}: {e}")
        return []

def extract_content_info(json_data):
    return {
        "content_title": json_data.get("content title"),
        "summary_of_articles": json_data.get("summary_of_articles"),
        "conclusion": json_data.get("conclusion")
    }

def extract_sources_info(json_data):
    return json_data.get("sources_cited", [])

@app.after_request
async def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
async def home():
    return await render_template('uimock_flash.html')

@app.route('/news-analysis')
async def uimock_feed():
    selected_categories = session.get('selected_categories', [])
    current_date = datetime.now().strftime("%d %B")
    return await render_template('feed.html', selected_categories=selected_categories, current_date=current_date)

@app.route('/process-selection', methods=['POST'])
async def process_selection():
    selected_words = (await request.form).get('selectedWords', '')
    print(f"Selected words: {selected_words}")
    return redirect(url_for('feed'))

@app.route('/process_keywords', methods=['POST'])
async def process_keywords():
    keywords = (await request.form).get('typed_lines', '')
    session['keywords'] = keywords.split('\n')
    return redirect(url_for('uimock_flash'))

@app.route('/feed')
async def feed():
    current_date = datetime.now().strftime("%d %B")
    keywords = session.get('keywords', [])
    market_analysis_dir = 'data/marketAnalysis'
    market_data = []

    for filename in os.listdir(market_analysis_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(market_analysis_dir, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    market_data.append({
                        "filename": os.path.splitext(filename)[0],
                        "data": data.get('Data', {})
                    })
                except json.JSONDecodeError:
                    market_data.append({
                        "filename": os.path.splitext(filename)[0],
                        "data": {"Current Price": "N/A", "Moving Average": "N/A", "Trend": "N/A"}
                    })
                    
    print(market_data)
    return await render_template('feed.html', keywords=keywords, current_date=current_date, market_data=market_data)

specific_keywords = [
    "oil prices", "gas prices", "oil and gas stock market", "company news", "supply and demand", "production rates", "market news", "trading news",
    "commodity prices", "futures", "exploration", "refining", "pipelines", "oilfield services", "petroleum", "downstream", "upstream", "midstream",
    "LNG", "reserves", "drilling", "shale oil", "offshore drilling", "exports", "imports", "OPEC", "refining capacity", "production cuts", "consumption", "inventory"
]

@app.route('/suggest_keywords')
async def suggest_keywords():
    return Response(orjson.dumps(specific_keywords), mimetype='application/json')


@app.route('/split-screen2')
async def split_screen2():
    async with aiofiles.open('data/report/report/report.json') as report_file:
        report_data = orjson.loads(await report_file.read())
    
    async with aiofiles.open('data/report/sources/sources_ranked.json') as sources_file:
        sources_data = orjson.loads(await sources_file.read())
    
    return await render_template('split_screen2.html', report_data=report_data, sources_data=sources_data)

@app.route('/process_next', methods=['POST'])
async def process_next():
    data = await request.json
    keywords = data.get('keywords', '')
    selected_words = data.get('selectedWords', '')
    
    # Print to terminal
    print(f"Keywords: {keywords}")
    print(f"Selected Words: {selected_words}")
    
    # Write to input.txt
    async with aiofiles.open('data/userInput/input.txt', 'w') as file:
        await file.write(f"Keywords:\n{keywords}\n\nSelected Words:\n{selected_words}\n")
    
    # Store selected categories in session
    session['selected_categories'] = selected_words.split(',')
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)