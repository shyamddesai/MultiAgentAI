import json
import os
import subprocess
import logging
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify
from flask_caching import Cache
import ujson as json  # so many jasons :/
from flask_compress import Compress  # Gzip compression
from celery import Celery  # Celery for asynchronous tasks

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
Compress(app)  # Enable Gzip compression
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Configure Celery broker
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Configure Celery result backend
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'])
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@cache.memoize(timeout=120)  # Cache for 2 minutes
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
@cache.cached(timeout=120)
def home():
    return render_template('index.html')

@app.route('/pdf/<filename>')
def pdf(filename):
    return send_from_directory('pdfs', filename)

@app.route('/market-prediction')
def market_prediction():
    return "Market Prediction Page"

@app.route('/news-analysis')
def news_analysis():
    news_data = load_json_data('news_report.json')
    report_data = load_json_data('report.json')
    return render_template('news_analysis.html', news_data=news_data, report_data=report_data)

@app.route('/uimock_flash0')
@cache.cached(timeout=60)
def uimock_flash0():
    return render_template('uimock_flash0.html')

@app.route('/uimock_flash')
@cache.cached(timeout=60)
def uimock_flash():
    return render_template('uimock_flash.html')

@app.route('/uimock_loading')
@cache.cached(timeout=120)
def uimock_loading():
    return render_template('uimock_loading.html')

@app.route('/uimock_feed')
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
        return redirect(url_for('uimock_loading'))

specific_keywords = [
    "oil prices", "gas prices", "oil and gas stock market", "company news",
    "supply and demand", "production rates", "market news", "trading news",
    "commodity prices", "futures", "exploration", "refining", "pipelines",
    "oilfield services", "petroleum", "downstream", "upstream", "midstream",
    "LNG", "reserves", "drilling", "shale oil", "offshore drilling", "exports",
    "imports", "OPEC", "refining capacity", "production cuts", "consumption", "inventory"
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