import time
from .mpApi import *
from .utils import *
from ..pricestf import *
from alive_progress import alive_bar
import math

class MpSaleOptimizationService():
    def __init__(self):
        self.mpapi = MpApi()
    
    def getQualities(self):
        return mpUtils.TF2_QUALITIES

    def nonStockedItem(self, items, quality, dashboardItems, itemPrices, keypriceref, steamData, rateUSDEUR):
        cont = 0
        #Optimization
        scmItemsDict = {}
        for scmItem in steamData['data']:
            price = scmItem['prices']['safe_ts']['last_24h']
            if price == 0 or price == None: price = scmItem['prices']['safe_ts']['last_7d']

            avgSold = scmItem['prices']['sold']['last_24h']
            if avgSold == 0 or avgSold == None: avgSold = scmItem['prices']['sold']['avg_daily_volume']

            scmItemsDict[scmItem['market_hash_name']] = {
                'price': price*rateUSDEUR,
                'avg_sold':  avgSold}
                    
        
        print("Getting attributes for "+str(quality)+  " items and generating the Excel")
        with alive_bar(len(items[mpUtils.BIG_SKU])) as bar:
            for sku in items[mpUtils.BIG_SKU]:
                                 
                
                items[mpUtils.BACKPACK_URL][cont] = mpUtils.GLADIATOR_BACKPACK_URI+str(items[mpUtils.NAME][cont])

                itemName = str(items[mpUtils.NAME][cont])
                if itemName.startswith("The%20"):
                    itemName = itemName[6:]

                if quality != mpUtils.UNCRAFTABLE:
                    items[mpUtils.BACKPACK_URL][cont] = mpUtils.GLADIATOR_BACKPACK_URI+str(items[mpUtils.NAME][cont])
                    items[mpUtils.ADD_GLADIATOR][cont] = mpUtils.GLADIATOR_URI+str(items[mpUtils.NAME][cont])+mpUtils.ADD_URL

                elif quality == mpUtils.UNCRAFTABLE: 
                    items[mpUtils.BACKPACK_URL][cont] = mpUtils.GLADIATOR_BACKPACK__NON_CRAFTABLE_URI+str(items[mpUtils.NAME][cont])
                    items[mpUtils.ADD_GLADIATOR][cont] = mpUtils.GLADIATOR_URI_NON_CRAFTABLE+str(items[mpUtils.NAME][cont])+mpUtils.ADD_URL



                items[mpUtils.MARKETPLACE_URL][cont] = mpUtils.MARKETPLACE_URI+str(sku)
                

                for item in dashboardItems[mpUtils.ITEMS]:
                    itemFiltered = mpUtils.filterItem(item[mpUtils.SKU])
                    if (itemFiltered == sku):
                        items[mpUtils.QUANTITY][cont] = items[mpUtils.QUANTITY][cont]+item[mpUtils.NUM_FOR_SALE]

                if itemPrices is not None:
                    for itemPrice in itemPrices:
                        if itemPrice[mpUtils.SKU] == sku: 
                            items[mpUtils.BP_PRICE][cont] = mpUtils.convertPrice(itemPrice[mpUtils.BUY_HALF_SCRAP], itemPrice[mpUtils.BUY_KEYS], keypriceref)
                            break
                
                howManyBuy = items[mpUtils.HOW_MANY_BUY][cont]
                
                
                items[mpUtils.STOCK][cont] = howManyBuy - items[mpUtils.QUANTITY][cont]
                if(items[mpUtils.STOCK][cont]<0): items[mpUtils.STOCK][cont] = 0

                items[mpUtils.ADD_BOT][cont] = "sku="+str(sku)+"&max="+str(items[mpUtils.STOCK][cont])+"&min="+str(items[mpUtils.STOCK][cont]-1)+"&group="+str(items[mpUtils.HOW_MANY_BUY][cont])

                cont = cont+1
                bar()

        #print(mpUtils.FINISHED_ITEMS+str(quality))

        return items   
    
    def nonStockedItems(self, items, itemPrices, keypriceref, steamData, rateUSDEUR):
        qualities = mpUtils.TF2_QUALITIES
        dashboardItems = self.mpapi.getDashboardItems()
        itemsDict = {}

        
        for quality in qualities:
            df = self.nonStockedItem(items[quality], quality, dashboardItems, itemPrices, keypriceref, steamData, rateUSDEUR)
            itemsDict[quality] = df
        
        #### DEBUGGER
        '''
        df = self.nonStockedItem(items['Unique'], 'Unique', dashboardItems, itemPrices, keypriceref, steamData, rateUSDEUR)
        itemsDict['Unique'] = df
        '''
        return itemsDict

