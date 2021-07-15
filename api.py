# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# step by step explanation for setting up and running flask and what each statement means

import flask
from flask import request, jsonify, abort
from flask_cors import CORS
import pdfminer
from readers.pdf_reader import generateData

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

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
