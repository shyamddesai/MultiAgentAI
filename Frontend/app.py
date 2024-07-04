import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/market-prediction')
def market_prediction():
    return "Market Prediction Page"

@app.route('/news-analysis')
def news_analysis():
    try:
        with open('./reports/news_report.json') as f:
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    try:
        with open('report.json') as f:
            report_data = json.load(f)
    except FileNotFoundError:
        report_data = []
    return render_template('news_analysis.html', news_data=news_data, report_data=report_data)

@app.route('/feature-3')
def feature_3():
    return "Feature 3 Page"

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)