import flask
from flask import request, jsonify

import  FifaMachineLearning

app = flask.Flask(__name__)
app.config["DEBUG"] = True

response =  { "request": {}, "ids" : [], "message" : "" }

@app.route('/', methods=['GET'])
def home():
    return "<h1>My Python API</h1>"

@app.route('/api/v1/KNN', methods=["POST"])
def ClosestPlayer():

    #Check request...
    try:

        print(request.json)
        #Inputs
        id = request.json.get("playerID")
        n_neighbors = request.json.get("nNeighbors")
        ignore_nationality = request.json.get("ignoreNationality")
        type = request.json.get("playerType")

        #Create predicting object
        fifaML = FifaMachineLearning.FifaMachineLearning(int(n_neighbors), str(type), bool(ignore_nationality))

        response["request"] = dict(request.json)
        response["ids"] = fifaML.Closest(int(id))
        response["message"] = "OK"

        print(response)

        return jsonify(response)

    except Exception as exp:
        print(exp)
        return(jsonify({"request" : dict(request.json), "ids" : [], "message" : "Request Error!"}))


app.run()