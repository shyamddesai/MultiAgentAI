from flask import Flask,render_template, request, url_for, jsonify, make_response, abort
import json

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/data")
def data():
   with open('data.json') as f:
      data = json.load(f)
   return render_template('data.html', summary=data['summary'], chart_data=json.dumps(data['data']))

@app.route("/news")
def news():
   with open('news.json') as f:
      data = json.load(f)
   return render_template('news.html', news_data = data)

@app.route("/news2")
def news2():
   with open('reports/news_report.json') as f:
      data = json.load(f)
   return render_template('news2.html', news_data = data)


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp





if __name__ == '__main__':
   app.run(debug=True)