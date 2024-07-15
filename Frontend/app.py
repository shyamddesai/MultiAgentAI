import json
import subprocess
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
from flask_caching import Cache
import ujson as json  # so many jasons :/
from celery import Celery  # Celery for asynchronous tasks

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Configure Celery broker
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Configure Celery result backend
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'])

ICON_MAPPING = {
    "Company": "fa-building",
    "Exploration": "fa-compass",
    "Market Trends": "fa-chart-line",
    "Production Updates": "fa-industry",
    "Refining": "fa-oil-can",
    "Finance": "fa-dollar-sign",
    "Technology": "fa-microchip",
    "Health": "fa-heartbeat",
    "Environment": "fa-leaf",
    "Education": "fa-graduation-cap",
    "Sports": "fa-football-ball",
    "Market Analysis": "fa-chart-bar"
}

#@cache.memoize(timeout=120)  # Cache for 2 minutes
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        app.logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        app.logger.error(f"Error decoding JSON from file: {file_path}")
        return []

@app.route('/')
def home():
    return render_template('index.html')

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
@cache.cached(timeout=120)
def uimock_loading():
    return render_template('uimock_loading.html')

@app.route('/news-analysis')
def uimock_feed():
    #reportConversion('txt_to_json.py')
    return render_template('feed.html')


@app.route('/process-selection', methods=['POST'])
def process_selection():
    if 'typed_lines' in request.form:
        typed_lines = request.form['typed_lines']
        app.logger.info("Typed Lines: %s", typed_lines)
        return redirect(url_for('uimock_flash'))
    elif 'selected_avatars' in request.form:
        selected_avatars = request.form['selected_avatars']
        app.logger.info("Selected Avatars: %s", selected_avatars)
        return redirect(url_for('feed', selected_avatars=selected_avatars.split(',')))

@app.route('/feed')
def feed():
    selected_avatars = request.args.getlist('selected_avatars')
    return render_template('feed.html', selected_avatars=selected_avatars, icon_mapping=ICON_MAPPING)

specific_keywords = [
    "oil prices", "gas prices", "oil and gas stock market", "company news", "supply and demand", "production rates", "market news", "trading news",
    "commodity prices", "futures", "exploration", "refining", "pipelines", "oilfield services", "petroleum", "downstream", "upstream", "midstream",
    "LNG", "reserves", "drilling", "shale oil", "offshore drilling", "exports", "imports", "OPEC", "refining capacity", "production cuts", "consumption", "inventory"
]

@app.route('/suggest_keywords')
def suggest_keywords():
    return jsonify(specific_keywords)

def reportConversion(file_path):
    try:
        completed_process = subprocess.run(['python', file_path], capture_output=True, text=True)
        if completed_process.returncode == 0:
            app.logger.info("Execution successful.")
            app.logger.info("Output: %s", completed_process.stdout)
        else:
            app.logger.error(f"Error: Failed to execute '{file_path}'.")
            app.logger.error("Error output: %s", completed_process.stderr)
    except FileNotFoundError:
        app.logger.error(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    app.run(debug=True)