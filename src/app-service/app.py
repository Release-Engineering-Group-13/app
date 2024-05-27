from flask import Flask, jsonify, request
import requests
from flasgger import Swagger
import json
#from version_util import VersionUtil

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/get_prediction', methods =['GET'])    
def predict ():
    """
    Queries model-service to get prediction
    """
    link_text = request.args.get("input")
    link = {"link": f"{link_text}"}
   
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    
    response = requests.post("http://host.docker.internal:8080/predict", json=link, headers=headers)

    return jsonify(response.text)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)