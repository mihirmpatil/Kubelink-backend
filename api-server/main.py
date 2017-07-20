from flask import Flask, request, jsonify
from service_catalog_client import ServiceCatalogClient
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    return "Hello World!!!"

@app.route("/catalog/standalone")
def get_catalog():
    client = ServiceCatalogClient("bora-catalog")
    output = client.get_catalog()
    classes = output["items"]
    classesOp = []
    for item in output["items"]:
        d = {"name": item["metadata"]["name"]}
        d["imageSrc"]="img/kubernetes/k8s"
        d["id"]=item["externalID"]
        classesOp.append(d)
    resp = {}
    resp["status"] = "OK"
    resp["message"]="Successful"
    resp["data"] = classesOp
    return jsonify(resp)
        
app.run(host="0.0.0.0",port=5000,debug=True)




