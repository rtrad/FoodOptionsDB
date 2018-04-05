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
    first = True
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if first:
                first = False
                continue
            item = {}
            item['name'] = row[0]
            item['restaurant'] = {
                'name': restaurant,
                'location' : restaurant_location[restaurant]
            }
            item['nutrition'] = {}
            
            try:
                item['nutrition']['Calories'] = float(row[1])
            except:
                item['nutrition']['Calories'] = row[1]
            try:
                item['nutrition']['Calories From Fat'] = float(row[2])
            except:
                item['nutrition']['Calories From Fat'] = row[2]
            try:
                item['nutrition']['Total Fat (g)'] = float(row[3])
            except:
                item['nutrition']['Total Fat (g)'] = row[3]
            try:
                item['nutrition']['Saturated Fat (g)'] = float(row[4])
            except:
                item['nutrition']['Saturated Fat (g)'] = row[4]
            try:
                item['nutrition']['Trans Fat (g)'] = float(row[5])
            except:
                item['nutrition']['Trans Fat (g)'] = row[5]
            try:
                item['nutrition']['Cholesterol (mg)'] = float(row[6])
            except:
                item['nutrition']['Cholesterol (mg)'] = row[6]
            try:
                item['nutrition']['Sodium (mg)'] = float(row[7])
            except:
                item['nutrition']['Sodium (mg)'] = row[7]
            try:
                item['nutrition']['Carbohydrates (g)'] = float(row[8])
            except:
                item['nutrition']['Carbohydrates (g)'] = row[8]
            try:
                item['nutrition']['Fiber (g)'] = float(row[9])
            except:
                item['nutrition']['Fiber (g)'] = row[9]
            try:
                item['nutrition']['Sugars (g)'] = float(row[10])
            except:
                item['nutrition']['Sugars (g)'] = row[10]
            try:
                item['nutrition']['Protein (g)'] = float(row[11])
            except:
                item['nutrition']['Protein (g)'] = row[11]
            try:
                item['nutrition']['Vitamin A (% DV)'] = float(row[12])
            except:
                item['nutrition']['Vitamin A (% DV)'] = row[12]
            try:
                item['nutrition']['Vitamin C (% DV)'] = float(row[13])
            except:
                item['nutrition']['Vitamin C (% DV)'] = row[13]
            try:
                item['nutrition']['Calcium (% DV)'] = float(row[14])
            except:
                item['nutrition']['Calcium (% DV)'] = row[14]
            try:
                item['nutrition']['Iron (% DV)'] = float(row[15])
            except:
                item['nutrition']['Iron (% DV)'] = row[15]
            try:
                item['price'] = float(row[16])
            except:
                item['price'] = row[16]
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
