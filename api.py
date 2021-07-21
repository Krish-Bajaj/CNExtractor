# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# step by step explanation for setting up and running flask and what each statement means

import flask
from flask import request, jsonify, abort
from flask_cors import CORS
import pdfminer
from pymongo import MongoClient
import datetime
from readers.pdf_reader import generateData
import constants

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# connects to the database
client = MongoClient(constants.mongo_url)
db = client.Cluster1 # connects to the cluster
users = db.users # creates/accesses the users db

def sendData():
    key = { "key": "1234567" }
    userDocument = {
        "key": "1234567",
        "name": { "first": "kk", "last": "BBBB" },
        "birth": datetime.datetime(2001, 6, 1),
    }
    users.replace_one(key, userDocument, upsert=True)
    # "upsert" inserts new data if "key" isn't present otherwise updates current data

    # print(users.find_one({ "name.last": "B" })) # accessing data

# sendData()

@app.route('/contracts/all', methods=['GET', 'POST'])
def api_all():
    if request.method == 'POST':
        try:
            data_list = generateData(request.get_json()["password"])
            response = jsonify(data_list) # very important line - otherwise throws a type error
            return response
        except pdfminer.pdfdocument.PDFPasswordIncorrect as error:
            abort(505, description="Password is either not sent or incorrect")
    # request.form -> get normal data from the endpoint, with request.get_json() u get json data
    # which gets converted into a python dict

app.run()
