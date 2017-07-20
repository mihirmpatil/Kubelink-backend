import subprocess
import json

class ServiceCatalogClient(object):

    def __init__(self, contextName, counter=300):
        self.context = contextName
        self.decoder = json.JSONDecoder()
        self.counter = counter 
        
    def execute(self, cmd, read=False):
        newcmd = cmd + " --context "+self.context
        if read:
            newcmd += " -o json"
        jsonText = subprocess.check_output(newcmd, shell=True)
        if read:
            return self.decoder.decode(jsonText)
        else:
            return None

    def get_catalog(self):
        command = "kubectl get serviceclasses"
        return self.execute(command, True)

    def create_instance(self, service_class_name):
        r = open("instances/"+service_class_name.lower()+".yaml").read()
        r = r.replace("#name#",service_class_name.lower()+"--"+str(self.counter))
        f = open("instances/"+service_class_name.lower()+"-"+str(self.counter)+".yaml","w")
        f.write(r)
        f.close()
        command = "kubectl create -f " + "instances/"+service_class_name.lower()+"-"+str(self.counter)+".yaml"
        self.counter+=1
        self.execute(command)
        return True


def main():
    print ServiceCatalogClient("bora-catalog").create_instance("mysql")

#main()

        

