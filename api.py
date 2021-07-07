# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# step by step explanation for setting up and running flask and what each statement means

import flask
from flask import request, jsonify
from readers.pdf_reader import generateData

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]

df = generateData()
print(df)

@app.route('/books/all', methods=['GET'])
def api_all():
    # response = jsonify(books)
    # response.headers.add("Access-Control-Allow-Origin", "*")
    response = jsonify(df)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

app.run()