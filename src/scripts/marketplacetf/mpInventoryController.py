from .mpApi import *
from .utils import *
import pandas as pd
from alive_progress import alive_bar

class MpInventoryController():
    def __init__(self):
        self.mpapi = MpApi()

    def getTf2Price(self, sku, items, keypriceref):
        for item in items:
            itemFiltered = mpUtils.filterItem(item[mpUtils.SKU])
            if(itemFiltered == sku): return mpUtils.convertPrice(item[mpUtils.BUY_HALF_SCRAP], item[mpUtils.BUY_KEYS], keypriceref)
        return 0

    def getItemBackpackName(self, mpName):
        mpName = mpName.replace("Basic ","")
        mpName = mpName.replace("Specialized","Specialized Killstreak")
        if "Pithy" not in mpName:
            mpName = mpName.replace("Professional","Professional Killstreak")
        mpName = mpName.replace("Paint: ","")
        mpName = mpName.replace("★","")
        mpName = mpName.replace("Peace Sign","Circling Peace Sign")
        mpName = mpName.replace("TF Logo","Circling TF Logo")
        mpName = mpName.replace("Australium","Strange Australium")
        mpName = mpName.replace("Professional Killstreak Strange","Strange Professional Killstreak")
        mpName = mpName.replace("Specialized Killstreak Strange","Strange Specialized Killstreak")
        mpName = mpName.replace("Specialized Killstreak Strange","Strange Specialized Killstreak")
        mpName = mpName.replace("Killstreak Strange","Strange Killstreak")
        mpName = mpName.replace("Specialized Killstreak Vintage","Vintage Specialized Killstreak")
        mpName = mpName.replace("Specialized Killstreak Vintage","Vintage Specialized Killstreak")
        mpName = mpName.replace("Killstreak Vintage","Vintage Killstreak")
        mpName = mpName.replace("Specialized Killstreak Genuine","Genuine Specialized Killstreak")
        mpName = mpName.replace("Specialized Killstreak Genuine","Genuine Specialized Killstreak")
        mpName = mpName.replace("Killstreak Genuine","Genuine Killstreak")

        sheens = mpUtils.SHEENS
        effects = mpUtils.EFFECTS
        for sheen in sheens:
            repl = " ("+sheen+")"
            mpName = mpName.replace(repl,"")
            for effect in effects:
                repl = " ("+sheen+", "+effect+")"
                mpName = mpName.replace(repl,"")

        return mpName


    def checkAllNonProfitableItems(self):
        nonProfitableItems = pd.DataFrame(columns=[mpUtils.BIG_SKU, mpUtils.NAME, mpUtils.MP_URL, mpUtils.BACKPACK_PRICE_BUY, mpUtils.BACKPACK_PRICE_SELL, mpUtils.MARKETPLACE_PRICE, mpUtils.PROFIT])
        dashboardItems = self.mpapi.getDashboardItems()
        #itemPrices = self.pricestf.getAllItems()

        #cont = 0
        #keypriceref = self.pricestf.getKeyPriceRef()
        print("Getting estimated profit of all the items")
        with alive_bar(len(dashboardItems[mpUtils.ITEMS])) as bar:
            for item in dashboardItems[mpUtils.ITEMS]:
                skuFiltered = mpUtils.filterItem(item[mpUtils.SKU])
                mpName = item['name']
                mpNameFiltered = self.getItemBackpackName(mpName)
                BPprice = 0 #self.getTf2Price(itemFiltered, itemPrices, keypriceref)
                MPprice = item[mpUtils.PRICE]/100

                profit = 0
                if(BPprice != 0):
                    profit = ((MPprice*0.9)/mpUtils.KEYPRICEUSD)/BPprice

                newRow = pd.DataFrame({mpUtils.BIG_SKU: [skuFiltered],
                                    mpUtils.NAME: [mpNameFiltered],
                                    mpUtils.MP_URL: [mpUtils.MARKETPLACE_URI+skuFiltered],
                                    mpUtils.BACKPACK_PRICE_BUY: [BPprice],
                                    mpUtils.BACKPACK_PRICE_SELL: [BPprice],
                                    mpUtils.MARKETPLACE_PRICE: [MPprice],
                                    mpUtils.PROFIT: [profit]})
                
                nonProfitableItems = pd.concat([nonProfitableItems, newRow])
                bar()
                #cont = cont+1
                #if(cont>50): break
            
        print(nonProfitableItems)
        return(nonProfitableItems)