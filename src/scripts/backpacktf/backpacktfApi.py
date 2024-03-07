import requests
from .utils import backpackUtils as u
from .utils import backpackApikey as a

class BackpacktfApi:
    def uwu(self):
        return("xd")
    

    def getBackpackSnapshot(self, itemName):
        parameters = {
            u.TOKEN: a.BP_TOKEN,
            u.APPID: u.TF2_APPID,
            u.SKU: itemName
        }
        head = {'content-type': "application/json"}
        response = requests.get(u.BP_SNAPSHOTS_URI, params=parameters, headers=head).json()
        return response