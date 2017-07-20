from flask import Flask, request, jsonify
from service_catalog_client import ServiceCatalogClient
from flask_cors import CORS, cross_origin
import json
import etcd

app = Flask(__name__)
CORS(app)
etcd_client = etcd.Client(host='etcd.kubelink.borathon.photon-infra.com', port=80)
client = ServiceCatalogClient("bora-catalog", etcd_client)


@app.route("/")
def main():
    return "Hello World!!!"

@app.route("/catalog/standalone", methods=["GET"])
def get_catalog():
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
    servicename = request.args.get("name","")
    service_id = request.args.get("id","")
    resp = {}
    if servicename == "" :
        resp["status"] = "ERROR"
        resp["message"]="Invalid Service Name."
    else:
        servicename = servicename.lower().replace(" ","")
        instance_id = client.create_instance(servicename, service_id)
        # TODO insert into etcd here
        key_prefix = "/instances/standalone/"
        key = key_prefix + instance_id
        d = {"name" : servicename}
        d["id"] = instance_id
        d["status"] = "Creating"
        d["accessURL"] = ""
        d["credentials"] = ""
        etcd_client.write(key, json.dumps(d))

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




