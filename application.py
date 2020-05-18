# -*- coding: utf-8 -*-
#import datetime
#from hashlib import md5

#import pytz
#from flask import Flask, render_template, jsonify, request, \
    #abort, g, flash, session
#from werkzeug.security import check_password_hash, generate_password_hash
#from flask.ext.pymongo import pymongo
#import pandas as pd
#from bson.objectid import ObjectId

# read in data
#master_condensed = pd.read_csv("data/master_beer_condensed.csv")
#breweries = pd.read_csv("data/nc_breweries_df.csv")
#breweries_condensed = pd.read_csv("data/satallite_breweries_removed.csv")

# establish mongo db connection
##conn = 'mongodb://localhost:27017'
##client = pymongo.MongoClient(conn)
##db = client.nc_breweries_db

# drop existing collection to prevent duplicates
#db.master_condensed.drop()
#db.breweries.drop()
#db.breweries_condensed.drop()

# creates a collection and inserts data
#db.master_condensed.insert_many(master_condensed.to_dict('records'))
#db.breweries.insert_many(breweries.to_dict('records'))
#db.breweries_condensed.insert_many(breweries_condensed.to_dict('records'))

# import dependencies
from flask import Flask, render_template, jsonify
import pymongo
import pandas as pd
import math

# read in data
master = pd.read_csv("data/master_beer_df.csv")
master_condensed = pd.read_csv("data/master_beer_condensed.csv")
breweries = pd.read_csv("data/nc_breweries_df.csv")
breweries_condensed = pd.read_csv("data/satallite_breweries_removed.csv")

# establish mongo db connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.nc_breweries_db

# drop existing collection to prevent duplicates
db.beer_master.drop()
db.master_condensed.drop()
db.breweries.drop()
db.breweries_condensed.drop()

# creates a collection and inserts data
db.beer_master.insert_many(master.to_dict('records'))
db.master_condensed.insert_many(master_condensed.to_dict('records'))
db.breweries.insert_many(breweries.to_dict('records'))
db.breweries_condensed.insert_many(breweries_condensed.to_dict('records'))

app = Flask(__name__)

# setup mongodb
#mongo = PyMongo(app)
#client = pymongo.MongoClient
#db = client.nc_breweries_db

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/beerList')
def beerList():
    master = list(db.master_condensed.find({}, {'_id': False}))
    breweries = list(db.breweries_condensed.find({}, {'_id': False}))
    return render_template("beerList.html", master=master, breweries=breweries)

@app.route('/beerMap')
def beerMap():
    return render_template("beerMap.html")

@app.route('/geoData')
def geoData():
    breweries = list(db.breweries.find({}, {'_id': False}))
    allPoints = []
    for brewery in breweries:
        outGeoJson = {}
        del brewery["phone"]
        outGeoJson["properties"] = brewery
        outGeoJson["type"] = "Feature"
        outGeoJson["geometry"] = {"type": "Point", "coordinates": [brewery['longitude'], brewery['latitude']]}
        allPoints.append(outGeoJson)
    geoJSONs = {"type": "FeatureCollection", "features": allPoints}
    return jsonify(geoJSONs)

if __name__ == "__main__":
    app.run(debug=True)