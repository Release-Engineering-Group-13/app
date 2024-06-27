import os
from flask import Flask, jsonify, request, render_template, Response 
import requests
from flasgger import Swagger
import json
import sys
from flask_cors import CORS
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil 
#from version_util import VersionUtil

from REMLA_Test_Lib_version import VersionUtil


app = Flask(__name__)
swagger = Swagger(app)
CORS(app)  # This will enable CORS for all routes

REQUEST_COUNT = Counter('num_prediction_requests', 'Total number of prediction requests')
INDEX_REQUEST_COUNT = Counter('num_index_requests', 'Total number of index requests')
HTTP_STATUS_COUNT = Counter('num_bad_requests', 'Count per HTTP status code', ['status'])
REQUEST_TIME = Histogram('prediction_time', 'Total time taken to evaluate a url')
CPU_USAGE = Gauge('cpu_usage_percent', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Current memory usage in bytes')


response_url = os.environ.get("MODEL_SERVICE_URL", "http://host.docker.internal:8080")

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
        status = 400
        return jsonify({"error": "No input provided"}), status
    
    link = {"link": link_text}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    try:
        response = requests.post(response_url + "/predict", json=link, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        status = 500
        return jsonify({"error": str(e)}), status

    # Return the JSON response
    return jsonify(response.json())

@app.route('/', methods=['GET', 'POST'])
def index():
    INDEX_REQUEST_COUNT.inc()
    start_time = time.time()
    prediction = None
    if request.method == 'POST':
        link = request.form['link']
        response = requests.post(response_url + "/predict", json={'link': link})
        status = response.status_code 
        HTTP_STATUS_COUNT.labels(status=status).inc()
        if status == 200:
            prediction = response.json().get('Prediction')
            print("prediction: ", prediction)
            REQUEST_COUNT.inc()
    response_time = time.time() - start_time
    REQUEST_TIME.observe(response_time)
    return render_template('index.html', prediction=prediction)

@app.route('/metrics')
def metrics():
    """
    Defines /metrics route for Prometheus
    """
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)