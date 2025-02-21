import pandas as pd
import time
from .utils import csdealsUtils as u
from .csdealsApi import CsdealsApi
from alive_progress import alive_bar
from colorama import Fore, Style
from typing import Literal


pd.options.mode.chained_assignment = None  # default='warn'


class CsdealsService:
    def __init__(self):
        self.csdealsapi = CsdealsApi()

    def getAllSteamPricesGame(self, gameId, isCompact, compactValue=None):
        return self.csdealsapi.getAllSteamPricesGame(gameId, isCompact, compactValue)
    
    def getRustProfitableItemsCsdeals(self, appId, usdEur):
        csdealsItems = self.csdealsapi.getCsdealsPrice(appId)
        rustScmPrices = self.getAllSteamPricesGame(appId, False)
        profitableCsdealsItems = pd.DataFrame(columns=[u.ITEM_NAME,u.CSDEALS_PRICE, u.STEAM_PRICE, u.PROFIT, u.VOLUME_DAILY, u.VOLUME_WEEKLY])
        profitableCsdealsItemsBuyOrder = pd.DataFrame(columns=[u.ITEM_NAME,u.CSDEALS_PRICE, u.STEAM_PRICE_BUY_ORDER, u.PROFIT, u.VOLUME_DAILY, u.VOLUME_WEEKLY])


        breakCont = 0
        for rustItem in csdealsItems['response']['items']:
            for rustScmPrice in rustScmPrices['data']:
                if rustItem['marketname'] == rustScmPrice['market_hash_name']:
                    scmSafePrice7d = round(rustScmPrice['prices']['safe_ts']['last_7d']*usdEur, 2)

                    salesWeeklyAvg = rustScmPrice['prices']['sold']['last_7d']
                    salesDailyAVG = round(salesWeeklyAvg/7)

                    if salesDailyAVG == None: salesDailyAVG = 0

                    if salesDailyAVG < u.MINIMUM_VOLUME:
                        break

                    scmData = CsdealsApi().getScmDataRust(rustItem['marketname'])
                    
                    if scmData.get("histogram"):
                        scmLowestForSale = round(scmData["histogram"].get("lowest_sell_order", 0) * usdEur, 2) if scmData["histogram"].get("lowest_sell_order") is not None else None
                        scmBuyOrder = round(scmData["histogram"].get("highest_buy_order", 0) * usdEur, 2) if scmData["histogram"].get("highest_buy_order") is not None else None
                    else:
                        scmLowestForSale = None
                        scmBuyOrder = None


                    rustItemPrice = round(float(rustItem['lowest_price'])*usdEur, 2)

                    print(f"Item Name = {rustItem['marketname']} and SALES AVG = {salesDailyAVG}")

                    if scmLowestForSale == None or scmSafePrice7d < scmLowestForSale:
                        scmPrice = scmSafePrice7d
                    else:
                        scmPrice = scmLowestForSale


                    if scmPrice <= 0.21:
                        scmProfit = (scmPrice-0.02) / rustItemPrice
                    else:
                        scmProfit = (scmPrice/1.15) / rustItemPrice
                    
                    if scmBuyOrder == None:
                        scmProfitBuyOrder = 0   
                    elif scmBuyOrder <= 0.21:
                        scmProfitBuyOrder = (scmBuyOrder-0.02) / rustItemPrice
                    else:
                        scmProfitBuyOrder = (scmBuyOrder/1.15) / rustItemPrice

                    if scmProfit > u.MINIMUM_PROFIT and salesDailyAVG > u.MINIMUM_VOLUME:
                        newRow = pd.DataFrame({u.ITEM_NAME: [rustItem['marketname']],
                                                u.CSDEALS_PRICE: [rustItemPrice],
                                                u.STEAM_PRICE: [scmPrice], 
                                                u.PROFIT: [round(scmProfit, 2)],
                                                u.VOLUME_DAILY: [salesDailyAVG],
                                                u.VOLUME_WEEKLY: [salesWeeklyAvg]
                                                })
                        if not newRow.empty:
                            profitableCsdealsItems = pd.concat([profitableCsdealsItems, newRow], ignore_index=True)

                        
                    if scmProfitBuyOrder > u.MINIMUM_PROFIT_BUY_ORDER and salesDailyAVG >= u.MINIMUM_VOLUME:
                        newRowBuyOrder = pd.DataFrame({u.ITEM_NAME: [rustItem['marketname']],
                                                u.CSDEALS_PRICE: [rustItemPrice],
                                                u.STEAM_PRICE_BUY_ORDER: [scmBuyOrder], 
                                                u.PROFIT: [round(scmProfitBuyOrder, 2)],
                                                u.VOLUME_DAILY: [salesDailyAVG],
                                                u.VOLUME_WEEKLY: [salesWeeklyAvg]
                                                })
                        
                        if not newRowBuyOrder.empty:
                            profitableCsdealsItemsBuyOrder = pd.concat([profitableCsdealsItemsBuyOrder, newRowBuyOrder], ignore_index=True)

                    break
            #if breakCont > 100: break
            breakCont += 1
        

        profitableCsdealsItems = profitableCsdealsItems.sort_values(by=[u.PROFIT], ascending=False)
        print(profitableCsdealsItems)
        profitableCsdealsItemsBuyOrder = profitableCsdealsItemsBuyOrder.sort_values(by=[u.PROFIT], ascending=False)
        return profitableCsdealsItems, profitableCsdealsItemsBuyOrder
    
