import logging
import socket
from os import environ
from waitress import serve
from flask import Flask, render_template, request
from urllib.request import Request, urlopen
from urllib.error import URLError

app = Flask(__name__)

metadata_url = "http://metadata.google.internal/computeMetadata/v1"

# index
@app.route('/')
def index():
    app.logger.info(f"Request for / for {request.remote_addr} with {request.headers.get('User-Agent')}")
    cloud = True
    environment = ""
    instance_id = ""
    instance_name = ""
    instance_zone = ""

    if "GAE_APPLICATION" in environ:
        environment = "Running on Google App Engine!"
    elif environ.get('K_SERVICE'):
        environment = "Running on Cloud Run!"
    elif is_on_gce():
        environment = "Running on Google Compute Engine!"
    else:
        environment = "Not running on Google Cloud (or cannot be determined)!"
        cloud = False

    if cloud:
        instance_id = queryMetadata("/instance/id")
        instance_name = queryMetadata("/instance/name")
        instance_zone = queryMetadata("/instance/zone").rsplit('/', 1)[1]

    return render_template(
        'index.jinja',
        environment=environment,
        instance_id=instance_id,
        instance_name=instance_name,
        instance_zone=instance_zone,
    )

# helper function - generates the requested status code
@app.route('/status/<code>')
def status(code):
    app.logger.info(f"Returning HTTP Status Code: {code} for {request.remote_addr} with {request.headers.get('User-Agent')}")
    return ("Returned HTTP Status Code: " + code, code)

def queryMetadata(attribute):
    req = Request(metadata_url + attribute)
    req.add_header("Metadata-Flavor", "Google")
    try:
        return urlopen(req).read().decode()
    except URLError as e:
        return "Metadata entry not found."
    
def is_on_gce():
    try:
        socket.getaddrinfo('metadata.google.internal', 80)
    except socket.gaierror:
        return False
    return True


if __name__ == "__main__":
    logging.getLogger('waitress').setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    serve(app, host='0.0.0.0', port=environ.get('PORT', '8080'))
