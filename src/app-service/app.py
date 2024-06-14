import os
from flask import Flask, jsonify, request, render_template
import requests
from flasgger import Swagger
import json
import sys
from flask_cors import CORS
#from version_util import VersionUtil

from REMLA_Test_Lib_version import VersionUtil


app = Flask(__name__)
swagger = Swagger(app)
CORS(app)  # This will enable CORS for all routes


response_url = os.environ.get("MODEL_SERVICE_URL", "http://host.docker.internal:8080/predict")

@app.route('/get_version', methods=['GET'])
def version():
    """
    Returns the version of the service
    ---
    responses:
      200:
        description: Version of the service
    """
    return jsonify({"version": VersionUtil.VersionUtil.get_version()})

@app.route('/get_prediction', methods=['GET'])
def predict():
    """
    Queries model-service to get prediction
    """
    link_text = request.args.get("input")
    if not link_text:
        return jsonify({"error": "No input provided"}), 400
    
    link = {"link": link_text}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    try:
        response = requests.post(response_url, json=link, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # Return the JSON response
    return jsonify(response.json())

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        link = request.form['link']
        response = requests.post(response_url, json={'link': link})
        if response.status_code == 200:
            prediction = response.json().get('Prediction')
            print(prediction)
    
    return render_template('index.html', prediction=prediction)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)