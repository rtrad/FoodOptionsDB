from flask import Flask, request, render_template, json
from bson import json_util, objectid
from pymongo import MongoClient



dbclient = MongoClient('localhost', 27017)
db = dbclient.foodoptionsdb

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compare', methods=['GET'])
def compare_items():
    ids = map(lambda x: objectid.ObjectId(x), request.args.get('ids').split(','))
    
    items = db.foods.find({'_id' : {'$in' : ids}})
    return render_template('food_item.html', items=items)

    
@app.route('/fooditem/<id>')
def food_item(id):
    item = db.foods.find_one({'_id' : objectid.ObjectId(id)})
    return render_template('food_item.html', items=[item])
    
    
@app.route('/search', methods=['POST'])
def search():
    text = request.form['textvalue'].strip()
    if len(text) > 0:
        items = db.foods.find({'$text' : {'$search' : request.form['textvalue']}})
    else:
        items = db.foods.find({})
        
    locations = items.distinct('restaurant')
    return json_util.dumps({'items' : items, 'locations' : locations})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
