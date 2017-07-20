from flask import Flask, request, jsonify
from service_catalog_client import ServiceCatalogClient
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    return "Hello World!!!"

@app.route("/catalog/standalone", methods=["GET"])
def get_catalog():
    client = ServiceCatalogClient("bora-catalog")
    output = client.get_catalog()
    classes = output["items"]
    classesOp = []
    for item in output["items"]:
        d = {"name": item["metadata"]["name"]}
        d["imageSrc"]="img/kubernetes/"+d["name"].lower().replace(" ","")
        d["id"]=item["externalID"]
        classesOp.append(d)
    resp = {}
    resp["status"] = "OK"
    resp["message"]="Successful"
    resp["data"] = classesOp
    return jsonify(resp)

@app.route("/catalog/standalone", methods=["POST"])
def create_instance():
    client = ServiceCatalogClient("bora-catalog",400)
    servicename = request.args.get("name","")
    resp = {}
    if servicename == "" :
        resp["status"] = "ERROR"
        resp["message"]="Invalid Service Name."
    else:
        client.create_instance(servicename.lower().replace(" ",""))
        resp["status"] = "OK"
        resp["message"]="Successful"
    return jsonify(resp)
        

def get_success_response(data):
    resp = {}
    resp["status"] = "OK"
    resp["message"]="Successful"
    resp["data"] = data
    return jsonify(resp)

def get_error_response(message):
    resp = {}
    resp["status"] = "ERROR"
    resp["message"]= message
    return jsonify(resp)

app.run(host="0.0.0.0",port=80,debug=True)




