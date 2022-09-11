from flask import Flask, request, jsonify
app = Flask(__name__)
import pymongo
import datetime
import pandas as pd 
from prophet import Prophet

myclient = pymongo.MongoClient("mongodb+srv://littytitties:litastits11@cluster0.7yrcb.mongodb.net/Cluster0?retryWrites=true&w=majority")
mydb = myclient["Cluster0"]
userCol = mydb["user"]
aIdCol = mydb["aId"]

def distillery(email):
    myquery = { "email": email }
    x = userCol.find_one(myquery)
    dump = x["predictionDump"]
    carrier = {}
    keys = list(dump.keys())
    for i in range(0, len(keys)):
        first = dump[keys[i]]
        goodsBundle = first['goods']
        transactionAppID = first['aId']
        for j in range(0, len(goodsBundle)):
            firstGood = goodsBundle[j]
            goodOfInterest = firstGood['aId']
            # if no array named goodOfInterest, create one
            if goodOfInterest not in carrier:
                carrier[goodOfInterest] = []
            carrier[goodOfInterest].append(transactionAppID)
    print(carrier, "carrier")
    return carrier

def midnight(data):
    #each key in data is the good, the values are instances of transactions they occur in
    # get keys
    carrier = {}

    keys = list(data.keys())
    # for each key, get the values
    for i in range(0, len(keys)):
        print(keys[i], "key")
        # get the values
        values = data[keys[i]]
        # for each value, get the appID
        for j in range(0, len(values)):
            print(values[j], "value")
            myquery = { "aId": values[j] }
            x = aIdCol.find_one(myquery)
            epoch1 = x["time"]
            print(epoch1, "epoch123")
            #BROKEN
            dateIs = (datetime.datetime.fromtimestamp(float(epoch1)/1000).strftime('%Y-%m-%d'))

            
            #convert epoch to date



            ammount = 0
            getToGoods = x["goods"]
            for k in range(0, len(getToGoods)):
                if getToGoods[k]["aId"] == keys[i]:
                    ammount = getToGoods[k]["requested"]
            goodOfInterest = keys[i]
            if goodOfInterest not in carrier:
                carrier[goodOfInterest] = []
            carrier[goodOfInterest].append([dateIs, ammount])


    return carrier

def predict(data, email): 
    print(data, "data")
    keys = list(data.keys())
    for i in range(0, len(keys)):
        print(keys[i], [i], "key1234")
        dataFrame = pd.DataFrame(data[keys[i]], columns = ['ds', 'y'])
        #if two rows or less in dataFrame, return
        if len(dataFrame) <= 2:
            print("nah")
        else:
            print(dataFrame, "dataFrame")
            model = Prophet()
            model.fit(dataFrame)

            future = model.make_future_dataframe(periods=2)
            forecast = model.predict(future)
            print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(), "forecast")
            #check row 0 yhat value        
            prediction = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
            # convert to valid bson object
            prediction = prediction.to_dict('records')
            print(prediction, "prediction")
            #create object with key of good and value of prediction


            # myquery = { "email": email }

            name = keys[i]
            predictions = prediction
            # place name and predictions in object
            object = {name: predictions}
            print(object, "object")


            
            # insert into mongodb under user
            myquery = { "email": email }
            userCol.update_one(myquery, {"$set": {"predcition": object}})







def returnData(email):
    print("1234", email)
    myquery = { "email": email }
    x = userCol.find_one(myquery)
    print(x['_id'])
    
    
    return str(x['_id'])


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    name = request.args.get("name", None)

    # For debugging
    print(f"Received: {name}")

    response = {}

    # Check if the user sent a name at all working
    if not name:
        response["ERROR"] = "No name found. Please send a name." 
    # Check if the user entered a number
    elif str(name).isdigit():
        response["ERROR"] = "The name can't be numeric. Please send a string."
    else:
        distilled = distillery(name)
        midnighted = midnight(distilled)
        predict(midnighted, name)
        x = returnData(name)
        response["MESSAGE"] = f"Welcome {name} {x} to our awesome API!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome API!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True)