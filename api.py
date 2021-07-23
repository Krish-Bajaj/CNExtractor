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

user_id = ''

def sendData(user_id):
    key = { "user_id": user_id }
    userDocument = {
        "user_id": user_id,
    }
    users.replace_one(key, userDocument, upsert=True)
    # "upsert" inserts new data if "key" isn't present otherwise updates current data

    # print(users.find_one({ "name.last": "B" })) # accessing data

@app.route('/user', methods=['POST'])
def get_data():
    user_id = request.get_json()["key"]
    response = jsonify(user_id)
    sendData(user_id)
    return 'works' # for any request there has to be some sort of a return statement else it'll throw an error

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
