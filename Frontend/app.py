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
<<<<<<< Updated upstream
        with open('news_report.json') as f:
=======
        with open('fastAPI/news_report.json') as f:
>>>>>>> Stashed changes
            news_data = json.load(f)
    except FileNotFoundError:
        news_data = []
    return render_template('news_analysis.html', news_data=news_data)

@app.route('/feature-3')
def feature_3():
    return "Feature 3 Page"
<<<<<<< Updated upstream
=======

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)