from flask import Flask, render_template_string
import requests
import socket
import subprocess
from googleapiclient import discovery
from google.auth import compute_engine

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>MIG Info</title>
</head>
<body>
    <h1>MIG Info</h1>
    <ul>
        <li>Private IP: {{ private_ip }}</li>
        <li>Hostname: {{ hostname }}</li>
        <li>Current MIG Size: {{ mig_size }}</li>
    </ul>
</body>
</html>
"""


@app.route("/")
def index():
    # Private IP
    private_ip = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip",
        headers={"Metadata-Flavor": "Google"}
    ).text

    hostname = socket.gethostname()

    # MIG Size
    credentials = compute_engine.Credentials()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/project/project-id",
        headers={"Metadata-Flavor": "Google"}
    ).text
    region = "europe-west3"
    mig_name = "si-mig"

    mig = service.regionInstanceGroupManagers().get(
        project=project,
        region=region,
        instanceGroupManager=mig_name
    ).execute()

    mig_size = mig.get("targetSize", "unknown")

    return render_template_string(HTML_TEMPLATE,
                                  private_ip=private_ip,
                                  hostname=hostname,
                                  mig_size=mig_size)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
