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
    project_id = queryMetadata("/project/project-id")
    instance_id = queryMetadata("/instance/id")
    instance_name = queryMetadata("/instance/name")
    instance_hostname = queryMetadata("/instance/hostname")

    return render_template(
        'index.jinja',
        project_id=project_id,
        instance_hostname=instance_hostname,
        instance_id=instance_id,
        instance_name=instance_name,
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