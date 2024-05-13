from flask import Flask, jsonify, request
import requests
from flasgger import Swagger
#from version_util import VersionUtil

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/predict', methods =['GET'])    
def predict ():
    """
    Queries model-service to get prediction
    """
    response = requests.get("0.0.0.0:8080/predict").json()
    print(response)
    return jsonify(response)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)