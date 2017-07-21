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

@app.route("/runninginstances", methods=["GET"])
def running_instances():
    #TODO get latest info using kubectl
    key = "/instances/standalone"
    #TODO get bundles also from etcd
    output = etcd_client.read(key, recursive=True)
    instances = []
    for item in output.children:
        temp = item.key.split('/')
        if len(temp) < 4:
            continue
        instance_id = temp[-1]
        final_status = client.get_pod(instance_id)
        d = json.loads(item.value)
        d["status"] = final_status
        instances.append(d)

    resp = {}
    resp["status"] = "OK"
    print json.dumps(instances)
    resp["data"] = json.dumps(instances)
    return jsonify(resp)


@app.route("/catalog/standalone", methods=["POST"])
def create_instance():
    #servicename = request.form["name"]
    #service_id = request.form["id"]
    servicename = request.get_json()["name"]
    service_id = request.get_json()["id"]
    resp = {}
    print "Create instance flask: ", servicename, service_id
    if service_id == "" :
        resp["status"] = "ERROR"
        resp["message"]="Invalid Service ID."
    else:
        servicename = servicename.lower().replace(" ","")
        instance_id = client.create_instance(servicename, service_id)
        # TODO insert into etcd here
        key_prefix = "/instances/standalone/"
        key = key_prefix + instance_id
        d = {"name" : servicename}
        d["id"] = instance_id
        d["status"] = "Creating"
        d["access_url"] = ""
        d["credential"] = ""
        d["bundle"] = ""
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

@app.route("/catalog/bundles", methods = ["GET"])
def get_bundle_catalog():
    top_level_key = "/bundles"
    bundle_lists = etcd_client.read(top_level_key,recursive=True).children
    l = []
    for bundle in bundle_lists:
        etcd_info = json.loads(bundle.value)
        data = {}
        data["types"] = etcd_info["types"]
        data["name"] = etcd_info["name"]
        data["id"] = etcd_info["id"]
        data["imageSrc"]= "/img/kubernetes/k8s-bundle"
        data["components"] = []
        for typename in data["types"]:
            #TODO: filter standalone services by types
            data["components"].append({})
            data["components"][-1][typename] = get_standalone_services(typename) 
        l.append(data)
    return get_success_response(l)
    
def get_standalone_services(typename):
    top_level_key = "/standalone/"+typename
    l = []
    try:
        service_list = etcd_client.read(top_level_key,recursive=True).children
        for service in service_list:
            etcd_info = json.loads(service.value)
            svc = {}
            svc["name"]=etcd_info["name"]
            svc["id"]=service.key.split("/")[-1]
            svc["imageSrc"]=etcd_info["photo"]
            l.append(svc)
    except:
        print "Key not found "+top_level_key

    return l

@app.route("/catalog/bundles/<int:id>")
def get_bundle(id):
    top_level_key = "/bundles/"+str(id)
    bundle = etcd_client.read(top_level_key)
    etcd_info = json.loads(bundle.value)
    data = {}
    data["types"] = etcd_info["types"]
    data["name"] = etcd_info["name"]
    data["id"] = etcd_info["id"]
    data["imageSrc"]= etcd_info["photo"]
    data["components"] = []
    for typename in data["types"]:
        data["components"].append({})
        data["components"][-1][typename] = get_standalone_services(typename) 
    return get_success_response(data)
    
@app.route("/catalog/bundles",methods=["POST"])
def create_bundle():
    input = request.get_json()
    bundle_id = input["id"]
    bundle_info = etcd_client.read("/bundles/"+str(bundle_id)).value
    bundle_name = bundle_info["name"]+"-"+str(client.get_and_update_counter())
    secret_name = bundle_info["name"]+"-secret-"+str(client.get_and_update_counter())

    typename = bundle_info["types"][0]
    type_instance_id = input[typename]["id"]
    type_instance_name = input[typename]["name"].lower().replace(" ","")
    instance_id = client.create_instance(type_instance_name,type_instance_id)
    # TODO insert into etcd here
    key_prefix = "/instances/standalone/"
    key = key_prefix + instance_id
    d = {"name" : type_instance_name}
    d["id"] = instance_id
    d["status"] = "Creating"
    d["access_url"] = ""
    d["credential"] = ""
    d["bundle"] = bundle_name
    etcd_client.write(key, json.dumps(d))
    binding_id = client.create_binding(secret_name, instance_id)

    typename = bundle_info["types"][1]
    type_instance_id = input[typename]["id"]
    type_instance_name = input[typename]["name"].lower().replace(" ","")
    instance_id = client.create_instance(type_instance_name,type_instance_id,secret_name)
    # TODO insert into etcd here
    key_prefix = "/instances/standalone/"
    key = key_prefix + instance_id
    d = {"name" : type_instance_name}
    d["id"] = instance_id
    d["status"] = "Creating"
    d["access_url"] = ""
    d["credential"] = ""
    d["bundle"] = bundle_name
    etcd_client.write(key, json.dumps(d))
    return get_success_response({})

        



app.run(host="0.0.0.0",port=5000,debug=True)




