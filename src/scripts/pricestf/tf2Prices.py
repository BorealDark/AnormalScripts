import requests
from .utils import pricestfUtils as u
from .utils import errorMessagesPricestf as e
from .pricestfApi import PricestfApi
import time
from alive_progress import alive_bar

class Tf2PricesService():
    def __init__(self):
        self.pricestfapi = PricestfApi()

    def getAllItems(self, isTest):
        page = 1
        limit = 100 

        response = self.pricestfapi.getItemsPageRequest(page, limit)

        if isTest: totalPages = 1
        else: totalPages = response[u.META][u.TOTAL_PAGES]
        items = []
        print("Getting TF2 prices")
        with alive_bar(totalPages) as bar:
            while(page <= totalPages):
                try:
                    itemsPage =  self.pricestfapi.getItemsPageRequest(page, limit)[u.ITEMS]
                    for item in itemsPage:
                        items.append(item)
                    page = page + 1
                    #print("page "+str(page)+" done")
                    time.sleep(2)
                except:
                    print(e.API_NOT_RESPONDING_PRICESTF)
                    time.sleep(30)
                bar()
        
        print ("ITEMS LEN = " +str(len(items)))
        return items
    
    def getItemPrice(self, sku, keypriceref):
        return self.pricestfapi.getPrice(sku, keypriceref)
    
    def getKeyPriceRef(self):
        return self.pricestfapi.getKeyPrice()/18
    
