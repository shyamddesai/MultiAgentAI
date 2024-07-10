import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

@app.route('/')
async def home():
    return render_template('index.html')

@app.route('/market-prediction')
async def market_prediction():
    return "Market Prediction Page"

@app.route('/news-analysis')
async def news_analysis():
    # Adjust the path to get the base directory of the root of the project
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    news_report_path = os.path.join(BASE_DIR, 'reports', 'news_report.json')
    filtered_news_report_path = os.path.join(BASE_DIR, 'reports', 'filtered_news_report.json')

    try:
        with open(news_report_path) as f:
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    try:
        with open(filtered_news_report_path) as f:
            report_data = json.load(f)
    except FileNotFoundError:
        report_data = []
    return render_template('news_analysis.html', news_data=news_data, report_data=report_data)

@app.route('/uimock_flash0')
async def uimock_flash0():
    return render_template('uimock_flash0.html')

@app.route('/uimock_flash')
async def uimock_flash():
    return render_template('uimock_flash.html')

@app.route('/uimock_loading')
async def uimock_loading():
    return render_template('uimock_loading.html')

@app.route('/uimock_feed')
async def uimock_feed():
    # Adjust the path to get the root directory of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_path = os.path.join(base_dir, 'Frontend', 'content.json')
    sources_path = os.path.join(base_dir, 'Frontend', 'sources.json')
    
    content = load_json_data(content_path)
    sources = load_json_data(sources_path)

    return render_template('uimock_feed.html', content=content, sources=sources)

@app.route('/uimock_navbar')
async def uimock_navbar():
    return render_template('uimock_navbar.html')

@app.route('/process-selection', methods=['POST'])
async def process_selection():
    if 'typed_lines' in request.form:
        typed_lines = request.form['typed_lines']
        print("Typed Lines: " + typed_lines)
        return redirect(url_for('uimock_flash'))
    elif 'selected_avatars' in request.form:
        selected_avatars = request.form['selected_avatars']
        print("Selected Avatars: " + selected_avatars)
        return redirect(url_for('uimock_loading'))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)