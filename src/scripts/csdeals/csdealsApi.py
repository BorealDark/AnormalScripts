from .utils import csdealsApikey
import requests
#from ...datamanager import dataManager as dm
from .utils import csdealsUtils as u
import http.client
import base64
from typing import Literal
from typing import List
import http.client
import time




class CsdealsApi:
    def getCsdealsPrice(self, appId):
        parameters = {
            u.KEY: csdealsApikey.CSDEALSAPIKEY,
            u.APPID: appId,
        }
        head = {'content-type': "application/json"}
        uri = u.API_GETLOWESTPRICES_CSDEALS

        response = requests.get(uri, params=parameters, headers=head).json()
        return response
    
    def getAllSteamPricesGame(self, appid, compactBoolean, compactValue):
        if compactBoolean == True:
            parameters = {
                "api_key": csdealsApikey.STEAMAPIS_APIKEY,
                "format": "compact",
                "compact_value": compactValue
            }
        else:
            parameters = {
                "api_key": csdealsApikey.STEAMAPIS_APIKEY,
            }

        head = {'content-type': "application/json"}
        uri = u.URI_STEAMAPI_SCM+str(appid)
        response = requests.get(uri, params=parameters, headers=head).json()
        return response
    
    def getScmDataRust(self, itemName):
        parameters = {
            "api_key": csdealsApikey.STEAMAPIS_APIKEY
        }
        head = {'content-type': "application/json"}
        uri = u.STEAMAPIS_ITEM_URI_RUST+itemName
        response = requests.get(uri, params=parameters, headers=head).json()
        time.sleep(60/u.STEAMAPIS_CALLS_MINUTE)
        return response