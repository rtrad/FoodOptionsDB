from flask import Flask, request, render_template, json, session
from bson import json_util, objectid
from pymongo import MongoClient
from passlib.hash import sha256_crypt



dbclient = MongoClient('localhost', 27017)
db = dbclient.foodoptionsdb

app = Flask(__name__)
app.secret_key = 'asdk32nv8h3<V;Sbioba3uu?;ASD;FatBV8>BWQFIB'

def text_validate(form_data):
    return isinstance(form_data, unicode) or isinstance(form_data, str)

def range_validate(form_data):
    return isinstance(form_data, dict) and 'min' in form_data and 'max' in form_data and \
        isinstance(form_data['min'], (int, long, float, complex)) and \
        isinstance(form_data['max'], (int, long, float, complex))

def list_validate(form_data):
    return isinstance(form_data, list)
    
def text_construction(field, form_data):
    return {'$text' : {'$search' : form_data}} if len(form_data.strip()) > 0 else {}
    
def range_construction(field, form_data):
    return {field : {'$gte' : form_data['min'], '$lte' : form_data['max']}}

def list_construction(field, form_data):
    return {'$or' : [{field : value} for value in form_data]}

def exclusion_list_construction(field, form_data):
    return {field : {'$nin' : form_data}}
    
def rating_construction(field, form_data):
    return {'$where' : "this['rating count'] > 0 && (this['rating sum']/this['rating count']) >= {} && (this['rating sum']/this['rating count']) <= {}".format(form_data['min'], form_data['max'])}
    
available_filters = {
    'text' : {'type' : 'text'},
    'price' : {'type' : 'range'}, 
    'restaurant.name' : {'type' : 'list'},
    'allergens' : {'type' : 'exclusion_list'},
    'nutrition.Calories' : {'type' : 'range'},
    'nutrition.Calories From Fat' : {'type' : 'range'},
    'nutrition.Total Fat (g)': {'type' : 'range'},
    'nutrition.Saturated Fat (g)' : {'type' : 'range'},
    'nutrition.Trans Fat (g)' : {'type' : 'range'},
    'nutrition.Cholesterol (mg)' : {'type' : 'range'},
    'nutrition.Sodium (mg)' : {'type' : 'range'},
    'nutrition.Carbohydrates (g)' : {'type' : 'range'},
    'nutrition.Fiber (g)' : {'type' : 'range'},
    'nutrition.Sugars (g)' : {'type' : 'range'},
    'nutrition.Protein (g)' : {'type' : 'range'},
    'nutrition.Vitamin A (% DV)' : {'type' : 'range'},
    'nutrition.Vitamin C (% DV)' : {'type' : 'range'},
    'nutrition.Iron (% DV)' : {'type' : 'range'},
    'nutrition.Calcium (% DV)': {'type' : 'range'},
    'rating' : {'type' : 'rating'}
}
filter_validation = {
    'text' : text_validate,
    'range' : range_validate,
    'list' : list_validate,
    'exclusion_list' : list_validate,
    'rating' : range_validate
}
filter_construction = {
    'text' : text_construction,
    'range' : range_construction,
    'list' : list_construction,
    'exclusion_list' : exclusion_list_construction,
    'rating' : rating_construction
}

@app.route('/')
def index():
    items = db.foods.distinct('restaurant.name')
    if 'logged-in' in session and session['logged-in'] and 'username' in session:
        return render_template('index.html', username=session['username'], restaurants=items)
    return render_template('index.html', restaurants=items)


@app.route('/compare', methods=['GET'])
def compare_items():
    ids = map(lambda x: objectid.ObjectId(x), request.args.get('ids').split(','))
    
    items = db.foods.find({'_id' : {'$in' : ids}})
    return render_template('food_item.html', items=items, pagetype='compare')

                
@app.route('/fooditem/<id>')
def food_item(id):
    item = db.foods.find_one({'_id' : objectid.ObjectId(id)})
    pipeline = []
    
    # text_search = item['name'] + ''.join(map(lambda x: ' '+x, item['tags']))
    text_search = ' '.join(item['tags'])
    # pipeline.append({'$match' : {'$text' : {'$search' : text_search}, '_id' : {'$ne' : objectid.ObjectId(id)}}})
    pipeline.append({'$match' : {'tags' : {'$in' : item['tags']}, '_id' : {'$ne' : objectid.ObjectId(id)}}})
    
    project = {'_id' : 1, 'name' : 1, 'tagSimilarity' : {'$size' : {'$setIntersection' : [item['tags'], '$tags']}}}
    if not isinstance(item['price'], str) and not isinstance(item['price'], unicode):
        project['price_dist'] = {'$abs' : {'$subtract' : [item['price'], '$price']}}
    pipeline.append({'$project' : project})    
    pipeline.append({'$sort' : {'tagSimilarity' : -1, 'price_dist' : 1}})
    pipeline.append({'$project' : {'_id' : 1, 'name' : 1}})
    pipeline.append({'$limit' : 5})
    
    # return str(pipeline)
    similar = db.foods.aggregate(pipeline)
    similar = list(similar)
    
    return render_template('food_item.html', items=[item], similar_items=similar)

    
@app.route('/advancedsearch', methods=['POST'])
def advanced_search():
    filter_expression = {}
    data = json.loads(request.data)['payload']
    
    for filter in data.iterkeys():
        if filter in available_filters and \
            filter_validation[available_filters[filter]['type']](data[filter]):
            exp = filter_construction[available_filters[filter]['type']](filter, data[filter])
            filter_expression.update(exp)
    items = db.foods.find(filter_expression)
    locations = items.distinct('restaurant')
    return json_util.dumps({'items' : items, 'locations' : locations})
    
    
@app.route('/search', methods=['POST'])
def search():
    text = request.form['textvalue'].strip()
    if len(text) > 0:
        items = db.foods.find({'$text' : {'$search' : request.form['textvalue']}})
    else:
        items = db.foods.find({})
        
    locations = items.distinct('restaurant')
    return json_util.dumps({'items' : items, 'locations' : locations})

    
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)['payload']
    username = data['username']
    password = data['password']
    p = db.users.find_one({'username' : username})
    if 'password' in p:
        p = p['password']
        if sha256_crypt.verify(password, p):
            session['logged-in'] = True
            session['username'] = username
            return json_util.dumps({'username' : username}), 200
    return json_util.dumps({'error' : 'authentication failed'}), 401
      
      
@app.route('/logout', methods=['POST'])
def logout():
    session['logged-in'] = False
    del session['username']
    return json_util.dumps({}), 200

    
@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)['payload']
    username = data['username']
    password = sha256_crypt.hash(data['password'])
    exists = db.users.find_one({'username' : username})
    if not exists:
        db.users.insert({'username' : username, 'password' : password, 'ratings' : {}})
        session['logged-in'] = True
        session['username'] = username
        return json_util.dumps({'username' : username}), 200
    return json_util.dumps({'error' : 'username already exists'}), 401
    
    
@app.route('/rate', methods=['POST'])
def rate():
    data = json.loads(request.data)['payload']
    id = data['id']
    value = data['value']
    if 'logged-in' in session and session['logged-in'] and 'username' in session:
        current_rating = db.users.find_one({'username' : session['username'], 'ratings.{}'.format(id) : {'$exists' : True}}, {'_id' : 0, 'ratings.{}'.format(id) : 1});
        if current_rating:
            current_rating = current_rating['ratings'][id]
            db.users.update({'username': session['username']}, {'$set' : {'ratings.{}'.format(id) : value}})
            rating_difference = value - current_rating
            db.foods.update({'_id' : objectid.ObjectId(id)}, {'$inc' : {'rating sum' : rating_difference}})
            return json_util.dumps({'success' : 'updated rating from {} to {}'.format(current_rating, value)}), 200
        else:
            db.users.update({'username' : session['username']}, {'$set' : {'ratings.{}'.format(id) : value}})
            db.foods.update({'_id' : objectid.ObjectId(id)}, {'$inc' : {'rating sum' : value, 'rating count' : 1}})
            return json_util.dumps({'success' : 'adding rating of {}'.format(value)}), 200
    return json_util.dumps({'error' : 'must be logged in'}), 401

        
@app.route('/tag', methods=['POST'])
def tag():
    data = json.loads(request.data)['payload']
    tag = data['tag']
    id = data['id']
    if 'logged-in' in session and session['logged-in'] and 'username' in session:
        db.foods.update({'_id' : objectid.ObjectId(id)}, {'$addToSet' : {'tags' : tag}})
        return json_util.dumps({}), 200
    return json_util.dumps({'error' : 'must be logged in'}), 401
        
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
