import subprocess
import json

class ServiceCatalogClient(object):

    def __init__(self, contextName):
        self.context = contextName
        self.decoder = json.JSONDecoder()
        
    def execute(self, cmd):
        newcmd = cmd + " -o json --context "+self.context
        jsonText = subprocess.check_output(newcmd, shell=True)
        return self.decoder.decode(jsonText)

    def get_catalog(self):
        command = "kubectl get serviceclasses"
        return self.execute(command)



def main():
    print str(ServiceCatalogClient("bora-catalog").get_catalog())

#main()

        

