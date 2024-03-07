import pandas as pd
from .utils import lootfarmUtils as u
from .lootfarmapi import LootfarmApi
import time
from alive_progress import alive_bar
import math

class LootFarmService:
    def __init__(self):
        self.lootfarmapi = LootfarmApi()
    
    def getLootfarmRustItems(self):
        marketInfo = LootfarmApi().getLootFarmRust()
        return marketInfo
    
    def getLootFarmTfItems(self):
        marketInfo = LootfarmApi().getLootFarmTf()
        return marketInfo

    def reduceLootfarmItems(self, lootFarmItems, gameId):
        reducedLootfarmItems = pd.DataFrame(columns=[u.ITEM_NAME, u.LOOTFARM_PRICE, u.LOOTFARM_QUANTITY, u.RATE])
        
        if gameId == 252490:
            for lootfarmItem in lootFarmItems:
                if lootfarmItem["have"] > 0 and lootfarmItem['price'] >= u.MINIMUM_RUST_PRICE:
                    newRow = pd.DataFrame({u.ITEM_NAME: [lootfarmItem['name']], 
                                                                        u.LOOTFARM_PRICE: [lootfarmItem['price']/100],
                                                                        u.LOOTFARM_QUANTITY: [lootfarmItem['have']],
                                                                        u.RATE: [lootfarmItem['rate']]
                                                                        })
                    reducedLootfarmItems = pd.concat([reducedLootfarmItems, newRow])
        
        elif gameId == 440:
            for lootfarmItem in lootFarmItems:
                if lootfarmItem["have"] > 0 and lootfarmItem['price'] >= u.MINIMUM_TF_PRICE:
                    newRow = pd.DataFrame({u.ITEM_NAME: [lootfarmItem['name']], 
                                                                        u.LOOTFARM_PRICE: [lootfarmItem['price']/100],
                                                                        u.LOOTFARM_QUANTITY: [lootfarmItem['have']],
                                                                        u.RATE: [lootfarmItem['rate']]
                                                                        })
                    reducedLootfarmItems = pd.concat([reducedLootfarmItems, newRow])

        return reducedLootfarmItems
    
    def getAllSteamPricesGame(self, gameId, isCompact, compactValue=None):
        return LootfarmApi().getAllSteamPricesGame(gameId, isCompact, compactValue)
    
    def getProfitableLootfarmItems(self, lootFarmItemsReduced, SteamPrices, rateUSDEUR, gameId):
        profitableLootfarmItems = pd.DataFrame(columns=[u.ITEM_NAME,u.STEAM_PRICE, u.LOOTFARM_PRICE, u.VOLUME, u.LOOTFARM_QUANTITY, u.SCM_BALANCE_RATE])
        
        for index, row in lootFarmItemsReduced.iterrows():
            try: 
                itemName = row['item_name']
                #print(row['item_name'])
                for steamItemPrice in SteamPrices['data']:
                    if steamItemPrice['market_hash_name'] == itemName:
                        priceTs = steamItemPrice['prices']['safe_ts']['last_24h']
                        priceLatest = steamItemPrice['prices']['latest']
                        steamPrice = priceTs
                        #if priceTs > priceLatest: steamPrice = priceTs
                        #else: steamPrice = priceLatest 
                        steamPrice = round(steamPrice, 2)
                        salesAVG = steamItemPrice['prices']['sold']['avg_daily_volume']
                        lootFarmPrice = 0
                        if(gameId == 570 or gameId == 730):
                            lootFarmPrice = math.ceil(((row['lootfarm_price']*1.03)*100))/100
                        else: lootFarmPrice = row['lootfarm_price']


                        scmBalanceRate = 0
                        loss = lootFarmPrice/(steamPrice*0.88)
                        keyRate = u.KEY_PRICE_LOOTFARM / u.KEY_PRICE_USD

                        scmBalanceRate = round(keyRate/loss, 2)

                        if salesAVG >= u.MINIMUM_DAILY_SALES_SCM:
                            newRow = pd.DataFrame({u.ITEM_NAME: [itemName],
                                                    u.STEAM_PRICE: [steamPrice], 
                                                    u.LOOTFARM_PRICE: [lootFarmPrice],
                                                    u.VOLUME: [salesAVG],
                                                    u.LOOTFARM_QUANTITY: [row['lootfarm_quantity']],
                                                    u.SCM_BALANCE_RATE: [scmBalanceRate]
                                                    })
                            
                            profitableLootfarmItems = pd.concat([profitableLootfarmItems, newRow])
                        break
            except: print("Item "+itemName+" has no price")

        profitableLootfarmItems = profitableLootfarmItems.sort_values(by=[u.SCM_BALANCE_RATE], ascending=False)
        print(profitableLootfarmItems)
        return profitableLootfarmItems
               
    
    def getCurrency(self, rates, currency):
        return u.getCurrency(rates, currency)
    
    
    