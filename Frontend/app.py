import subprocess
import orjson
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, Response, session
from flask_caching import Cache
from celery import Celery
from datetime import datetime

app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'])
app.secret_key = 'your_secret_key'  # Needed for session management

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return orjson.loads(file.read())
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
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def index():
    return render_template('index1.html')

@app.route('/pdf/<filename>')
def pdf(filename):
    return send_from_directory('pdfs', filename)

@app.route('/market-prediction')
def market_prediction():
    return "Market Prediction Page"

@app.route('/news-analysis-keywords')
def uimock_flash0():
    return render_template('uimock_flash0.html')

@app.route('/news-analysis-category')
def uimock_flash():
    return render_template('uimock_flash.html')

@app.route('/news-analysis-loading')
def uimock_loading():
    return render_template('uimock_loading.html')

@app.route('/news-analysis')
def uimock_feed():
    return render_template('feed.html')

@app.route('/process-selection', methods=['POST'])
def process_selection():
    selected_words = request.form.get('selectedWords', '')
    print(f"Selected words: {selected_words}")
    return redirect(url_for('feed'))

@app.route('/process_keywords', methods=['POST'])
def process_keywords():
    keywords = request.form.get('typed_lines', '')
    session['keywords'] = keywords.split('\n')
    return redirect(url_for('uimock_flash'))

@app.route('/feed')
def feed():
    current_date = datetime.now().strftime("%d/%m/%y")
    keywords = session.get('keywords', [])
    return render_template('feed.html', keywords=keywords, current_date=current_date)

specific_keywords = [
    "Natural Gas", "Oil Prices", "Gas Prices", "Oil and Gas Stock Market", "Oilfield Services", "Petroleum", "Downstream", "Upstream", "Midstream",
    "LNG", "Reserves", "Drilling", "Shale Oil", "Offshore Drilling", "Exports", "Imports", "OPEC", "Refining Capacity", "Production Cuts", "Consumption", "Inventory",
    "Crude Oil", "Asia", "Russia", "China", "India", "USA", "Middle East", "Africa", "Europe", "Latin America", "Canada", "Australia",
    "Naphtha", "Gasoline", "Diesel", "Jet Fuel", "Kerosene", "LPG", "Ethane", "Propane", "Butane", "Petrochemicals", "Plastics", "Fertilizers", "Solvents",
    "ADNOC", "ExxonMobil", "Shell", "BP", "Chevron", "Total", "Saudi Aramco", "Gazprom", "Rosneft", "PetroChina", "Sinopec", "ONGC", "Petrobras",
    
]

@app.route('/suggest_keywords')
def suggest_keywords():
    return Response(orjson.dumps(specific_keywords), mimetype='application/json')

@app.route('/split-screen')
def split_screen():
    json_data_1 = load_json_data('content.json')
    json_data_2 = load_json_data('sources.json')
    
    # Extract necessary information
    json_data_1 = extract_content_info(json_data_1)
    json_data_2 = extract_sources_info(json_data_2)
    
    return render_template('split_screen.html', json_data_1=json_data_1, json_data_2=json_data_2)

@app.route('/split-screen1')
def split_screen1():
    content_data = load_json_data('content.json')
    news_data = load_json_data('news_ranking.json')
    
    return render_template('split_screen1.html', content_data=content_data, news_data=news_data)

@app.route('/split-screen2')
def split_screen2():
    with open('report.json') as report_file:
        report_data = orjson.loads(report_file.read())
    
    with open('news_ranking.json') as sources_file:
        sources_data = orjson.loads(sources_file.read())
    
    return render_template('split_screen2.html', report_data=report_data, sources_data=sources_data)

def reportConversion(file_path):
    try:
        completed_process = subprocess.run(['python', file_path], capture_output=True, text=True)
        if completed_process.returncode == 0:
            app.logger.info("Execution successful. Output: %s", completed_process.stdout)
        else:
            app.logger.error(f"Error executing '{file_path}': {completed_process.stderr}")
    except FileNotFoundError:
        app.logger.error(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    app.run(debug=True)