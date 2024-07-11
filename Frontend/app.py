import json
import os
import subprocess
import logging
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@cache.memoize(timeout=120)  # Cache for 2 minutes
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
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

@app.route('/news-analysis')
def news_analysis():
    news_data = load_json_data('news_report.json')
    report_data = load_json_data('report.json')
    return render_template('news_analysis.html', news_data=news_data, report_data=report_data)

@app.route('/uimock_flash0')
def uimock_flash0():
    return render_template('uimock_flash0.html')

@app.route('/uimock_flash')
def uimock_flash():
    return render_template('uimock_flash.html')

@app.route('/uimock_loading')
def uimock_loading():
    return render_template('uimock_loading.html')

@app.route('/uimock_feed')
def uimock_feed():
    #content = load_json_data('content.json')
    #sources = load_json_data('sources.json')
    #return render_template('uimock_feed.html', content=content, sources=sources)
    reportConversion('txt_to_json.py')
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
    "oil prices", "gas prices", "oil and gas stock market", "oil company news",
    "oil and gas supply and demand", "oil production rates", "gas production rates",
    "energy market news", "oil trading news", "gas trading news", "crude oil prices",
    "natural gas prices", "commodity prices", "oil futures", "gas futures",
    "exploration", "refining", "pipelines", "oilfield services", "petroleum",
    "downstream", "upstream", "midstream", "LNG", "oil reserves", "drilling",
    "shale oil", "offshore drilling", "oil exports", "oil imports", "OPEC",
    "oil refining capacity", "oil production cuts", "oil consumption", "oil inventory"
]

@app.route('/suggest_keywords')
def suggest_keywords():
    return json.dumps(specific_keywords)

def reportConversion(file_path):
    try:
        completed_process = subprocess.run(['python', file_path], capture_output=True, text=True)
        if completed_process.returncode == 0:
            print("Execution successful.")
            print("Output:")
            print(completed_process.stdout)
        else:
            print(f"Error: Failed to execute '{file_path}'.")
            print("Error output:")
            print(completed_process.stderr)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    

if __name__ == '__main__':
    app.run(debug=True)