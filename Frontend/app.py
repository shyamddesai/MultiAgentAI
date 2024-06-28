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
        with open('news_report.json') as f:
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    return render_template('news_analysis.html', news_data=news_data)

@app.route('/feature-3')
def feature_3():
    return "Feature 3 Page"

if __name__ == '__main__':
    app.run(debug=True)