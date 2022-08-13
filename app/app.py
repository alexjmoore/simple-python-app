import logging
from os import environ
from waitress import serve
from flask import Flask, render_template
from urllib.request import Request, urlopen
from urllib.error import URLError

app = Flask(__name__)

metadata_url = "http://metadata.google.internal/computeMetadata/v1"

@app.route('/')
def index():
    instance_id = queryMetadata("/instance/id")
    instance_name = queryMetadata("/instance/name")
    instance_zone = queryMetadata("/instance/zone").rsplit('/', 1)[1]

    return render_template(
        'index.jinja',
        instance_id=instance_id,
        instance_name=instance_name,
        instance_zone=instance_zone,
    )

def queryMetadata(attribute):
    req = Request(metadata_url + attribute)
    req.add_header("Metadata-Flavor", "Google")
    try:
        return urlopen(req).read().decode()
    except URLError as e:
        return "Metadata entry not found."

if __name__ == "__main__":
    logging.getLogger('waitress').setLevel(logging.INFO)
    serve(app, host='0.0.0.0', port=environ.get('PORT', '8080'))
