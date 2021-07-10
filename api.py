# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# step by step explanation for setting up and running flask and what each statement means

import flask
from flask import request, jsonify
from readers.pdf_reader import generateData

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/contracts/all', methods=['GET'])
def api_all():
    data_list = generateData()
    response = jsonify(data_list)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run()
