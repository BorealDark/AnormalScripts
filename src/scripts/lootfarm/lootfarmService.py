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

    import pandas as pd

    def reduceLootfarmItems(self, lootFarmItems, gameId):
        # Lista para acumular filas antes de crear el DataFrame
        rows = []

        if gameId == 252490:
            min_price = u.MINIMUM_RUST_PRICE
        elif gameId == 440:
            min_price = u.MINIMUM_TF_PRICE
        else:
            return pd.DataFrame(columns=[u.ITEM_NAME, u.LOOTFARM_PRICE, u.LOOTFARM_MAX, u.LOOTFARM_QUANTITY, u.RATE])

        # Recorrer los ítems y filtrar
        for lootfarmItem in lootFarmItems:
            if lootfarmItem["have"] > 0 and lootfarmItem['price'] >= min_price:
                rows.append({
                    u.ITEM_NAME: lootfarmItem['name'], 
                    u.LOOTFARM_PRICE: lootfarmItem['price'] / 100,
                    u.LOOTFARM_QUANTITY: lootfarmItem['have'],
                    u.LOOTFARM_MAX: lootfarmItem['max'],
                    u.RATE: lootfarmItem['rate']
                })

        # Convertir la lista en un DataFrame (más eficiente que concat en cada iteración)
        return pd.DataFrame(rows, columns=[u.ITEM_NAME, u.LOOTFARM_PRICE, u.LOOTFARM_MAX, u.LOOTFARM_QUANTITY, u.RATE])

    
    def getAllSteamPricesGame(self, gameId, isCompact, compactValue=None):
        return LootfarmApi().getAllSteamPricesGame(gameId, isCompact, compactValue)
    

    def getProfitableLootfarmItems(self, lootFarmItemsReduced, SteamPrices, csdealsPrices, rateUSDEUR, gameId):
        profitableLootfarmItems = []

        for index, row in lootFarmItemsReduced.iterrows():
            try: 
                itemName = row[u.ITEM_NAME]
                for steamItemPrice in SteamPrices['data']:
                    if steamItemPrice['market_hash_name'] == itemName:
                        priceTs = steamItemPrice['prices']['safe_ts']['last_24h']
                        priceLatest = steamItemPrice['prices']['latest']

                        csdealsPrice = None
                        for csdealsItem in csdealsPrices['response']['items']:
                            if csdealsItem['marketname'] == itemName:
                                csdealsPrice = float(csdealsItem['lowest_price'])
                                break
                        
                        steamPrice = priceTs if priceTs != 0 else steamItemPrice['prices']['safe_ts']['last_7d']
                        steamPrice = round(steamPrice, 2)

                        salesAVG = steamItemPrice['prices']['sold']['last_30d'] / 30
                        if salesAVG < u.MINIMUM_DAILY_SALES_SCM:
                            break  

                        if gameId in [570, 730]:
                            lootFarmPrice = math.ceil(((row[u.LOOTFARM_PRICE] * 1.03) * 100)) / 100
                        else:
                            lootFarmPrice = row[u.LOOTFARM_PRICE]

                        loss = lootFarmPrice / (steamPrice * 0.88)
                        keyRate = u.KEY_PRICE_LOOTFARM / u.KEY_PRICE_USD
                        scmBalanceRate = round(keyRate / loss, 2)

                        if csdealsPrice:
                            csdealsToLootfarmRate = round((lootFarmPrice*0.97/csdealsPrice), 2)
                        else:
                            csdealsToLootfarmRate = None

                        profitableLootfarmItems.append({
                            u.ITEM_NAME: itemName,
                            u.STEAM_PRICE: steamPrice,
                            u.LOOTFARM_PRICE: lootFarmPrice,
                            u.CSDEALS_PRICE: csdealsPrice,
                            u.VOLUME: math.ceil(salesAVG),
                            u.LOOTFARM_QUANTITY: row[u.LOOTFARM_QUANTITY],
                            u.SCM_BALANCE_RATE: scmBalanceRate,
                            u.CSDEALS_TO_LF_RATE: csdealsToLootfarmRate,
                            u.HOW_MANY_CAN_DUMP_LF: max(0, row[u.LOOTFARM_MAX] - row[u.LOOTFARM_QUANTITY])
                        })
                        break  
            except Exception as e: 
                print(f"Item {itemName} has no price", e)

        profitableLootfarmItems_df = pd.DataFrame(profitableLootfarmItems)
        if not profitableLootfarmItems_df.empty:
            profitableLootfarmItems_df = profitableLootfarmItems_df.sort_values(by=[u.SCM_BALANCE_RATE], ascending=False)

        print(profitableLootfarmItems_df)
        return profitableLootfarmItems_df


        

               
    
    def getCurrency(self, rates, currency):
        return u.getCurrency(rates, currency)
    
    
    