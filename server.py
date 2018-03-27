from flask import Flask, request, render_template, json
from pymongo import MongoClient



dbclient = MongoClient('localhost', 27017)
db = db.client.foodoptionsdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
