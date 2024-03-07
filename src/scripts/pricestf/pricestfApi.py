import requests
from .utils import pricestfUtils as u
from .utils import errorMessagesPricestf as e
import time

apikey = ""
keyprice = 0.0

class PricestfApi():
    def getPrice(self, sku, keypriceref):
        global apikey
        
        head = {"accept": "application/json",
        "Authorization": "Bearer "+apikey
        }

        response = requests.get(u.API_PRICESTF_PRICE_ITEM+sku, headers=head).json()
        if u.STATUSCODE in response.keys() and response[u.STATUSCODE] == 401:
            self.getApiToken()
            head = {"accept": "application/json",
            "Authorization": "Bearer "+apikey
            }
            response = requests.get(u.API_PRICESTF_PRICE_ITEM+sku, headers=head).json()
            return self.convertPrice(response[u.BUY_HALF_SCRAP], response[u.BUY_KEYS], keypriceref)
        else:
            return self.convertPrice(response[u.BUY_HALF_SCRAP], response[u.BUY_KEYS], keypriceref)
        
    def getApiToken(self):    
        head = {"User-Agent":"Mozilla/5.0"}
        response = requests.post(u.API_PRICESTF_TOKEN, headers=head).json()
        global apikey
        apikey = response[u.ACCES_TOKEN]

    def getItemsPageRequest(self, page, limit):
        global apikey
        parameters = {
            u.PAGE: page,
            u.LIMIT: limit,
            u.ORDER: u.ORDER_ASC,
            u.ORDER_BY: u.CREATED_AT
        }    
        head = {"accept": "application/json",
        "Authorization": "Bearer "+apikey
        }

        response = requests.get(u.API_PRICESTF_PRICES, params=parameters, headers=head).json()
        if u.STATUSCODE in response.keys() and response[u.STATUSCODE] == 401:
            self.getApiToken()
            head = {"accept": "application/json",
            "Authorization": "Bearer "+apikey
            }
            response = requests.get(u.API_PRICESTF_PRICES, params=parameters, headers=head).json()
            return response
        else:
            return response
        
    def convertPrice(self, buyHalfScrap, buyKeys, keyprice):
        priceREF = buyHalfScrap/18
        priceKEYS = (priceREF/float(keyprice))+buyKeys
        return priceKEYS
    
    def getKeyPrice(self):
        global apikey
        
        head = {"accept": "application/json",
        "Authorization": "Bearer "+apikey
        }

        response = requests.get(u.API_PRICESTF_PRICE_ITEM+u.KEY_SKU, headers=head).json()
        if u.STATUSCODE in response.keys() and response[u.STATUSCODE] == 401:
            self.getApiToken()
            head = {"accept": "application/json",
            "Authorization": "Bearer "+apikey
            }
            response = requests.get(u.API_PRICESTF_PRICE_ITEM+u.KEY_SKU, headers=head).json()
            return response[u.BUY_HALF_SCRAP]
        else:
            return response[u.BUY_HALF_SCRAP]
        
    def keyPrice(self):
        global keyprice
        keyprice = float(self.getKeyPrice())