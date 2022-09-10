from flask import Flask, render_template, redirect, jsonify
import pymongo
import os
import sys


app = Flask(__name__)


@app.route('/')
def index():
    response = {}
    x = "a"
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