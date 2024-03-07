from scripts.pricestf import *
from scripts.marketplacetf import *
from scripts.lootfarm import *
from scripts.backpacktf import *
from datamanager.dataManager import *
from datamanager.dataManegerUtils import *

import requests

class Optimization():
    def getMarketplaceItems(self, checkPrices):
        rates = DataManegerService().excelToData(dataManegerUtils.PATH_RATES+dataManegerUtils.RATES+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.RATES)
        rateUSDEUR = LootFarmService().getCurrency(rates, "USD/EUR")


        qualities = MpSaleOptimizationService().getQualities()
        
        steamData = LootFarmService().getAllSteamPricesGame(440, False, None)
        items = {}
        for quality in qualities:
            items[quality] = DataManegerService().excelToData(dataManegerUtils().PATH_MARKETPLACE+dataManegerUtils().MP_ITEMS+dataManegerUtils().XSLX_EXTENSION, quality)
        
        itemPrices = None
        keypriceref = None
        if checkPrices == True:
            keypriceref = Tf2PricesService().getKeyPriceRef()
            itemPrices = Tf2PricesService().getAllItems(False)
        
        itemsQuantity = MpSaleOptimizationService().nonStockedItems(items, itemPrices, keypriceref, steamData, rateUSDEUR)


        for quality in qualities:
            DataManegerService().dataToExcel(dataManegerUtils.PATH_MARKETPLACE+dataManegerUtils.NON_STOCKED_ITEMS+str(quality)+dataManegerUtils().XSLX_EXTENSION, quality, itemsQuantity[quality])
        print("Excels generated.")

    def getNonProfitableMarketplaceItems(self):
                ### THIS IS IN CASE YOU WANT TO USE PRICES.TF (14 DAYS WITHOUT UPDATING PRICES LOL XD)
        #keypriceref = Tf2PricesService().getKeyPriceRef()
        #itemPrices = None #Tf2PricesService().getAllItems(False)
        
        mpItems = MpInventoryController().checkAllNonProfitableItems()
        DataManegerService().dataToExcel(dataManegerUtils.PATH_MARKETPLACE+dataManegerUtils.NON_PROFITABLE_ITEMS+dataManegerUtils.XSLX_EXTENSION, 
                                         dataManegerUtils.MP_ITEMS_SALE, 
                                         mpItems)
        
        mpItemsSale = DataManegerService().excelToData(dataManegerUtils.PATH_MARKETPLACE+dataManegerUtils.NON_PROFITABLE_ITEMS+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.MP_ITEMS_SALE)
        

        itemsNonProfitableBpPrices = BackpacktfService().getBackpackPricesMp(mpItemsSale)
        DataManegerService().dataToExcel(dataManegerUtils.PATH_MARKETPLACE+dataManegerUtils.NON_PROFITABLE_ITEMS+dataManegerUtils.XSLX_EXTENSION, 
                                         dataManegerUtils.NON_PROFITABLE_ITEMS_NAME, 
                                         itemsNonProfitableBpPrices)
        print("Non profitable items Excel have been generated")
        
    
    def lootfarm(self, gameId):  
        #RUST
        rates = DataManegerService().excelToData(dataManegerUtils.PATH_RATES+dataManegerUtils.RATES+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.RATES)
        rateUSDEUR = LootFarmService().getCurrency(rates, "USD/EUR")

        if (gameId == 252490): 
            #rustVolume = DataManegerService().excelToData(dataManegerUtils().PATH_CSDEALS+dataManegerUtils().PATH_RUST_VOLUME+dataManegerUtils().XSLX_EXTENSION, dataManegerUtils().RUST_PAGE)
            #profitableItemsAndVolume = LootFarmService().checkVolume(profitableItems, rustVolume)
            lootfarmRustItems = LootFarmService().getLootfarmRustItems()
            lootfarmRustItemsReduced = LootFarmService().reduceLootfarmItems(lootfarmRustItems, gameId)

            rustSteamPrices = LootFarmService().getAllSteamPricesGame(gameId, False)
            print (rustSteamPrices)
        
            profitableRustItems = LootFarmService().getProfitableLootfarmItems(lootfarmRustItemsReduced, rustSteamPrices, rateUSDEUR, gameId)
            #profitableItems = LootFarmService().lootFarmRust(rustSteamPrices)

            DataManegerService().dataToExcel(dataManegerUtils().PATH_LOOTFARM+dataManegerUtils().LOOTFARM_RUST+dataManegerUtils().XSLX_EXTENSION, dataManegerUtils().LOOTFARM_RUST, profitableRustItems)
            # Save updated quantity
            #DataManegerService().dataToExcel(dataManegerUtils().PATH_CSDEALS+dataManegerUtils().PATH_RUST_VOLUME+dataManegerUtils().XSLX_EXTENSION, 
            #                            dataManegerUtils().RUST_PAGE, 
            #                            profitableItemsAndVolume[1])

        if (gameId == 440):
            lootFarmTfItems = LootFarmService().getLootFarmTfItems()
            lootFarmTfItemsReduced = LootFarmService().reduceLootfarmItems(lootFarmTfItems, gameId)
            tfSteamPrices = LootFarmService().getAllSteamPricesGame(gameId, False)
            
            profitableTfItems = LootFarmService().getProfitableLootfarmItems(lootFarmTfItemsReduced, tfSteamPrices, rateUSDEUR, gameId)
            DataManegerService().dataToExcel(dataManegerUtils().PATH_LOOTFARM+dataManegerUtils().LOOTFARM_TF+dataManegerUtils().XSLX_EXTENSION, dataManegerUtils().LOOTFARM_TF, profitableTfItems)


    def bpbotoscm(self):
        #scmItems = DataManegerService().excelToData(dataManegerUtils.PATH_BACKPACKTF+dataManegerUtils.EXCEL_BACKPACKTF_SCM+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.EXCEL_BACKPACKTF_SCM)
        rates = DataManegerService().excelToData(dataManegerUtils.PATH_RATES+dataManegerUtils.RATES+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.RATES)
        rateUSDEUR = LootFarmService().getCurrency(rates, "USD/EUR")
        scmItems = LootFarmService().getAllSteamPricesGame(440, False, None)
        scmProfitableItems = BackpacktfService().getScmProfitableItems(scmItems, rateUSDEUR, True)
        DataManegerService().dataToExcel(dataManegerUtils().PATH_PROFITABLE_SCM_ITEMS+dataManegerUtils.SCM_PROFITABLE_TF2_ITEMS_BUY_ORDERS+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.SCM_PROFITABLE_TF2_ITEMS_BUY_ORDERS, scmProfitableItems)

    def bpsotoscm(self):
        rates = DataManegerService().excelToData(dataManegerUtils.PATH_RATES+dataManegerUtils.RATES+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.RATES)
        rateUSDEUR = LootFarmService().getCurrency(rates, "USD/EUR")
        scmItems = LootFarmService().getAllSteamPricesGame(440, False, None)
        scmProfitableItems = BackpacktfService().getScmProfitableItems(scmItems, rateUSDEUR, False)
        DataManegerService().dataToExcel(dataManegerUtils().PATH_PROFITABLE_SCM_ITEMS+dataManegerUtils.SCM_PROFITABLE_TF2_ITEMS_SELL_ORDERS+dataManegerUtils.XSLX_EXTENSION, dataManegerUtils.SCM_PROFITABLE_TF2_ITEMS_SELL_ORDERS, scmProfitableItems)
     


        

