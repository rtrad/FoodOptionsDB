import argparse
import csv
from pymongo import MongoClient

dbclient = MongoClient('localhost', 27017)
db = dbclient.foodoptionsdb

def main(file, restaurant):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            item = {}
            item['name'] = row[0]
            item['restaurant'] = restaurant
            item['nutrition'] = {}
            item['nutrition']['calories'] = int(row[1])
            item['nutrition']['calories_from_fat'] = int(row[2])
            item['nutrition']['total_fat'] = int(row[3])
            item['nutrition']['saturated_fat'] = float(row[4])
            item['nutrition']['trans_fat'] = int(row[5])
            item['nutrition']['cholesterol'] = int(row[6])
            item['nutrition']['sodium'] = int(row[7])
            item['nutrition']['carbohydrates'] = int(row[8])
            item['nutrition']['fiber'] = int(row[9])
            item['nutrition']['sugars'] = int(row[10])
            item['nutrition']['protein'] = int(row[11])
            item['nutrition']['vatamin_a'] = int(row[12])
            item['nutrition']['vitamin_c'] = int(row[13])
            item['nutrition']['calcium'] = int(row[14])
            item['nutrition']['iron'] = int(row[15])
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
