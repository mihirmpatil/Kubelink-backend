import json
import yaml
import etcd
import os
from service_catalog_client import ServiceCatalogClient
from constants import service_types

etcd_client = etcd.Client(host='etcd.kubelink.borathon.photon-infra.com', port=80)

yaml_template_file = "../etcd/service-instance-template.yaml"
with open(yaml_template_file, 'r') as stream:
    yaml_dict = yaml.load(stream)

#json_template = json.dumps(yaml_template)
#json_dict = json.loads(json_tempate)

standalone_prefix = "/standalone/"
photo_prefix = "img/kubernetes/"

catalog_client = ServiceCatalogClient("bora-catalog", etcd_client)
output = catalog_client.get_catalog()

for item in output["items"]:
    service_id = item["externalID"]
    service_name = item["metadata"]["name"].lower()
    service_type = service_types[service_name]
    key = standalone_prefix + service_type + "/" + service_id
    d = {"name" : service_name}
    d["type"] = service_type
    d["id"] = service_id
    d["photo"] = photo_prefix + service_name.lower().replace(" ", "")
    config_dict = yaml_dict
    config_dict["metadata"]["name"] = service_name
    config_dict["spec"]["serviceClassName"] = service_name
    d["config"] = config_dict
    #etcd_client.delete(key)
    etcd_client.write(key, json.dumps(d))

etcd_client.write("/counter", 0)

bundle_prefix = "/bundles/"
j = json.loads(open("instances/bundles.json").read())
for x in j["bootstrap"]:
    key = bundle_prefix + x["id"] 
    etcd_client.write(key, json.dumps(x))