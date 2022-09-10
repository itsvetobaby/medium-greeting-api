from flask import Flask, render_template, redirect, jsonify, request

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


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    name = request.args.get("name", None)
    print(f"Received: {name}")
    response = {}
    if not name:
        response["ERROR"] = "No name found. Please send a name."
    elif str(name).isdigit():
        response["ERROR"] = "The name can't be numeric. Please send a string."
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome API!"
    return jsonify(response)

if __name__=="__main__":
    app.run(threaded=True, debug=True, port=5001)