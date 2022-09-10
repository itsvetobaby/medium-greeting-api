from flask import Flask, render_template, redirect, jsonify
import pymongo
import os
import sys
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://littytitties:litastits11@cluster0.7yrcb.mongodb.net/Cluster0?retryWrites=true&w=majority")
mydb = myclient["Cluster0"]
mycol = mydb["user"]

app = Flask(__name__)


@app.route('/')
def index():
    response = {}
    myquery = { "email": "allinto@icloud.com" }
    x = mycol.find_one(myquery)
    x = (x['_id'])
    response["MESSAGE"] = f"Welcome {x} to our awesome API!"

    # Return the response in json format
    return jsonify(response)


# @app.route('/api/notes/mongo')
# def note_mongo():
#     notes = mongo.db.tasks.find()
#     data = []

#     for note in notes:
#         data.append({
#             '_id': str(note['_id']),
#             'content': note['content']
#         })

#     return jsonify(data)

if __name__=="__main__":
    app.run(threaded=True, debug=True, port=5001)