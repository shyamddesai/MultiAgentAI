from quart import Quart, render_template, request, redirect, session, url_for, Response
from datetime import datetime
import orjson
import aiofiles

app = Quart(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)
app.secret_key = 'your_secret_key'  # Needed for session management

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
    return await render_template('feed.html')

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
    current_date = datetime.now().strftime("%d/%m/%y")
    keywords = session.get('keywords', [])
    return await render_template('feed.html', keywords=keywords, current_date=current_date)

specific_keywords = [
    "oil prices", "gas prices", "oil and gas stock market", "company news", "supply and demand", "production rates", "market news", "trading news",
    "commodity prices", "futures", "exploration", "refining", "pipelines", "oilfield services", "petroleum", "downstream", "upstream", "midstream",
    "LNG", "reserves", "drilling", "shale oil", "offshore drilling", "exports", "imports", "OPEC", "refining capacity", "production cuts", "consumption", "inventory"
]

@app.route('/suggest_keywords')
async def suggest_keywords():
    return Response(orjson.dumps(specific_keywords), mimetype='application/json')

@app.route('/split-screen')
async def split_screen():
    json_data_1 = await load_json_data('content.json')
    json_data_2 = await load_json_data('sources.json')
    
    # Extract necessary information
    json_data_1 = extract_content_info(json_data_1)
    json_data_2 = extract_sources_info(json_data_2)
    
    return await render_template('split_screen.html', json_data_1=json_data_1, json_data_2=json_data_2)


@app.route('/split-screen2')
async def split_screen2():
    async with aiofiles.open('report.json') as report_file:
        report_data = orjson.loads(await report_file.read())
    
    async with aiofiles.open('news_ranking.json') as sources_file:
        sources_data = orjson.loads(await sources_file.read())
    
    return await render_template('split_screen2.html', report_data=report_data, sources_data=sources_data)

@app.route('/process_next', methods=['POST'])
async def process_next():
    keywords = await request.json.get('keywords')
    selected_words = await request.json.get('selectedWords')

    # Process the keywords and selected words here
    print(f"Keywords: {keywords}")
    print(f"Selected words: {selected_words}")

    # Redirect to the news-analysis page
    return redirect(url_for('uimock_feed'))

if __name__ == '__main__':
    app.run(debug=True)