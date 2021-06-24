import flask
from flask import request
import Models

app = flask.Flask(__name__)
app.config["DEBUG"] = True

model = Models.prediction_model()
model.load_model("trained_model.pkl")


"""This function accepts Post requests in the form of a list of dictionaries."""
@app.route('/read-json-multiple', methods=['POST'])
def predict_multiple():
    request_data = request.get_json()

    if type(request_data) != list:

        return "data needs to be a list of dictionaries"

    output = model.predict_JSON_multiple(request_data)

    return output

"""This function accepts Post requests in the form of a list of dictionaries."""
@app.route('/read-json-single', methods=['POST'])
def predict_single():
    request_data = request.get_json()

    if type(request_data) != dict:
        return "data needs to be a dictionary"
    output = model.predict_JSON_single(request_data)

    return output

app.run()