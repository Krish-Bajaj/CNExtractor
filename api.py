# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# step by step explanation for setting up and running flask and what each statement means

import flask
from flask import request, jsonify, abort
from flask_cors import CORS
import pdfminer
from pymongo import MongoClient
import datetime
import os
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
password = ''

def sendData(user_id):
    key = { "user_id": user_id }
    userDocument = { "$set": { "user_id": user_id } }
    users.update_one(key, userDocument, upsert=True)
    # "upsert" inserts new data if "key" isn't present otherwise updates current data

@app.route('/user', methods=['POST'])
def get_data():
    user_id = request.get_json()["key"]
    key = { "user_id": user_id }
    sendData(user_id)
    return 'works' # for any post request there has to be some sort of a return statement else it'll throw an error

@app.route('/contracts/all', methods=['GET', 'POST'])
def api_all():
    if request.method == 'POST':
        try:
            user_id = request.get_json()["key"]
            key = { "user_id": user_id }
            try:
                if users.find_one(key, { "_id": 0, "token": 1 }) != {}:
                    token_file = open('gmail_token.json', 'w')
                    token_file.write(users.find_one(key, { "_id": 0, "token": 1 })["token"])
                    token_file.close()
            except KeyError:
                print("New user!")

            if user_id != '':
                if users.find_one(key, { "_id": 0, "password": 1 }) != {}:
                    password = users.find_one(key, { "_id": 0, "password": 1 })["password"]
                else:
                    password = request.get_json()["password"]
                try:
                    data_list = generateData(password)
                except:
                    users.update_one(key, { "$unset" : { "password": 1 } })
                    password = request.get_json()["password"]
                    data_list = generateData(password)

            token_file = open('gmail_token.json', 'r')
            users.update_one(key, { "$set": { "token": token_file.read(), "password": password } }, upsert=True)
            token_file.close()
            os.remove('gmail_token.json')
            response = jsonify(data_list) # very important line - otherwise throws a type error
            return response
        except pdfminer.pdfdocument.PDFPasswordIncorrect as error:
            abort(505, description="Password is either not sent or incorrect")
    # request.form -> get normal data from the endpoint, with request.get_json() u get json data
    # which gets converted into a python dict

app.run()
