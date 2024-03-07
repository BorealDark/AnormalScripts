import requests
from .utils import lootfarmUtils as u
from .utils import steamapisApikey as a

class LootfarmApi:

    def getLootFarmRust(self):
        head = {'content-type': "application/json"}
        uri = u.URI_LOOTFARM_RUST

        response = requests.get(uri, headers=head).json()
        return response
    
    def getLootFarmDota(self):
        head = {'content-type': "application/json"}
        uri = u.URI_LOOTFARM_DOTA

        response = requests.get(uri, headers=head).json()
        return response
    
    def getLootFarmCs(self):
        head = {'content-type': "application/json"}
        uri = u.URI_LOOTFARM_CS

        response = requests.get(uri, headers=head).json()
        return response
    
    def getLootFarmTf(self):
        head = {'content-type': "application/json"}
        uri = u.URI_LOOTFARM_TF

        response = requests.get(uri, headers=head).json()
        return response
    
    def getAllSteamPrices(self, start, pagesize):
        parameters = {
                u.QUERY: u.RUST_APPID_SCM,
                u.START: start,
                u.COUNT: pagesize, #1 <= pagesize >= 100
                u.NORENDER: 1
            }
        head = {'content-type': "application/json"}

        response = requests.get(u.API_SCMRENDER_STEAM, params=parameters, headers=head).json()
        return response
    
    # Returns the price and volume on the SCM for the given item.
    # {'success': True, 'lowest_price': '0,96€', 'volume': '28', 'median_price': '0,86€'}
    def getSteamPrice(self, itemName):
        parameters = {
            u.APPID: u.RUST_APPID,
            u.CURRENCY: u.STEAM_EURO_CURRENCY,
            u.MARKET_HASH_NAME: itemName
        }
        head = {'content-type': "application/json"}
        uri = u.API_PRICEOVERVIEW_STEAM
        response = requests.get(uri, params=parameters, headers=head).json()
        return response
    
    def getAllSteamPricesGame(self, appid, compactBoolean, compactValue):
        if compactBoolean == True:
            parameters = {
                "api_key": a.STEAMAPI_APIKEY,
                "format": "compact",
                "compact_value": compactValue
            }
        else:
            parameters = {
                "api_key": a.STEAMAPI_APIKEY,
            }

        head = {'content-type': "application/json"}
        uri = u.URI_STEAMAPI_SCM+str(appid)
        response = requests.get(uri, params=parameters, headers=head).json()
        return response

