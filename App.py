import flask
from flask import request, jsonify
import pickle
import Models

app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = pickle.load(open('trained_model.pkl', 'rb'))

# Create some test data for our catalog in the form of a list of dictionaries.


@app.route('/json-example', methods=['POST'])
def predict():
    request_data = request.get_json()

    output = Models.predict_from_JSON(request_data)

    return output

app.run()