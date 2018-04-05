import argparse
import csv
from pymongo import MongoClient

dbclient = MongoClient('localhost', 27017)
db = dbclient.foodoptionsdb

restaurant_location = {
    'Chick-fil-a' : {
        'lat':33.773872, 
        'lng':-84.398900,
        'floor' : 1
    },
    'Panda Express' : {
        'lat':33.773670, 
        'lng':-84.398213,
        'floor' : 1
    },
    'Taco Bell' : {
        'lat':33.773807, 
        'lng':-84.398724,
        'floor' : 1
    }
}



def main(file, restaurant):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            item = {}
            item['name'] = row[0]
            item['restaurant'] = {
                'name': restaurant,
                'location' : restaurant_location[restaurant]
            }
            item['nutrition'] = {}
            item['nutrition']['Calories'] = int(row[1])
            item['nutrition']['Calories From Fat'] = int(row[2])
            item['nutrition']['Total Fat (g)'] = int(row[3])
            item['nutrition']['Saturated Fat (g)'] = int(row[4])
            item['nutrition']['Trans Fat (g)'] = int(row[5])
            item['nutrition']['Cholesterol (mg)'] = int(row[6])
            item['nutrition']['Sodium (mg)'] = int(row[7])
            item['nutrition']['Carbohydrates (g)'] = int(row[8])
            item['nutrition']['Fiber (g)'] = int(row[9])
            item['nutrition']['Sugars (g)'] = int(row[10])
            item['nutrition']['Protein (g)'] = int(row[11])
            item['nutrition']['Vitamin A (% DV)'] = int(row[12])
            item['nutrition']['Vitamin C (% DV)'] = int(row[13])
            item['nutrition']['Calcium (% DV)'] = int(row[14])
            item['nutrition']['Iron (% DV)'] = int(row[15])
            item['price'] = float(row[16])
            item['allergens'] = []
            if row[17] == '1':
                item['allergens'].append('dairy')
            if row[18] == '1':
                item['allergens'].append('soy')

            if row[19] == '1':
                item['allergens'].append('tree_nut')

            if row[20] == '1':
                item['allergens'].append('wheat')

            if row[21] == '1':
                item['allergens'].append('egg')




            db.foods.insert_one(item)
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('restaurant')
    args = parser.parse_args()
    main(args.file, args.restaurant)
