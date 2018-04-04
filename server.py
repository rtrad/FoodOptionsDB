from flask import Flask, request, render_template, json
from bson import json_util, objectid
from pymongo import MongoClient



dbclient = MongoClient('localhost', 27017)
db = dbclient.foodoptionsdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fooditem/<id>')
def food_item(id):
    item = db.foods.find_one({'_id' : objectid.ObjectId(id)})
    return render_template('food_item.html', item=item)
    
@app.route('/search', methods=['POST'])
def search():
    text = request.form['textvalue'].strip()
    if len(text) > 0:
        items = db.foods.find({'$text' : {'$search' : request.form['textvalue']}})
    else:
        items = db.foods.find({})
    return json_util.dumps(items)

if __name__ == '__main__':
    app.run(debug=True)
