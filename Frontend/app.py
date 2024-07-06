import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
async def home():
    return render_template('index.html')

@app.route('/market-prediction')
async def market_prediction():
    return "Market Prediction Page"

@app.route('/news-analysis')
async def news_analysis():
    try:
        with open('news_report.json') as f:
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    try:
        with open('report.json') as f:
            report_data = json.load(f)
    except FileNotFoundError:
        report_data = []
    return render_template('news_analysis.html', news_data=news_data, report_data=report_data)

@app.route('/uimock_feed')
async def uimock_feed():
    return render_template('uimock_feed.html')

@app.route('/uimock_flash')
async def uimock_flash():
    return render_template('uimock_flash.html')

@app.route('/process-selection', methods=['POST'])
async def process_selection():
    selected_avatars = request.form['selected_avatars']
    print("Selected Avatars: " + selected_avatars)
    return redirect(url_for('uimock_feed'))



    
if __name__ == '__main__':
    app.run(debug=True)