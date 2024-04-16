import requests
from .utils import  csgomarketUtils as u
from .utils import csgomarketApikey as a
import time

class CsgomarketApi:
    def getAllItems(self, str):
        head = {'content-type': "application/json"}

        if str == "sell": uri = u.CSGOMARKET_PRICELIST_API
        elif str == "buy": uri = u.CSGOMARKET_BUY_ORDERS_API

        response = requests.get(uri, headers=head).json()
        return response
    
    def getScmData(self, itemName):
        parameters = {
            "api_key": a.STEAMAPIS_APIKEY
        }
        head = {'content-type': "application/json"}
        uri = u.STEAMAPIS_ITEM_URI_CS2+itemName
        response = requests.get(uri, params=parameters, headers=head).json()
        time.sleep(0.6)
        return response
    
    def getCsgomarketItemInfo(self, itemName):
        parameters = {
            "key": a.CSGOMARKET_APIKEY,
            "list_hash_name[]": itemName
        }
        head = {'content-type': "application/json"}
        uri = u.CSGOMARKET_GET_LIST_ITEM_INFO_API
        response = requests.get(uri, params=parameters, headers=head).json()
        return response
        
