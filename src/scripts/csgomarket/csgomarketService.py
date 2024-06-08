from .csgomarketApi import CsgomarketApi
from .utils import csgomarketUtils as u
import pandas as pd
from datetime import datetime
from alive_progress import alive_bar
import time
import math


class CsgomarketService:
    def getAllItems(self, str):
        return CsgomarketApi().getAllItems(str)
        
    
    def getSellableSteamPrice(self, singleItemData, volume):
        price = 0
        cont = 0
        buyOrderPrice = singleItemData['histogram']['highest_buy_order']
        #print ("buy order price = "+str(buyOrderPrice))
        #print(singleItemData['histogram']['sell_order_array'])
        for prices in singleItemData['histogram']['sell_order_array']:
            if volume < 5:
                return prices['price']
            else:
                if price == 0: price = prices['price']
                else:  
                    #print(prices['price'])
                    newPrice = prices['price']

                    if buyOrderPrice*1.03 < newPrice:
                        cont = cont + prices['quantity']
                        if newPrice > price*1.05 or cont <= 3: price = newPrice
                        else: 
                            #print("Selected price = "+ str(price))
                            return price 
                    else: None
        #print("Selected price = "+ str(price))
        return price

    def checkIsBannedItem(self, itemName):
        for bannedItem in u.BANNED_ITEMS:
            if bannedItem in itemName:
                return True
        return False
    
    def getDictCsgomarketBuyOrders(self, csgomarketBuyOrders):
        buyOrdersDict = dict()
        for buyOrder in csgomarketBuyOrders['items']:
            buyOrdersDict[buyOrder['market_hash_name']] = float(buyOrder['price'])
        return buyOrdersDict

    def getCsgomarketItemInfo(self, itemName):
        return CsgomarketApi().getCsgomarketItemInfo(itemName)

    def getVolumeSalesMarketcsgo(self, itemName):
        listItems = [itemName]
        itemsData = self.getCsgomarketItemInfo(listItems)['data']

        now = datetime.now()
        timestampLast24Hours = int(datetime.timestamp(now) - 86400)
        volume = 0
        for key, index in itemsData[itemName]['history']:
            if key < timestampLast24Hours: break
            volume = volume + 1

        return volume


    def csgomarketScmDataProcesor(self, csgomarketData, csgomarketBuyOrders, scmItems, isFast, checkSalesCsgomarket):
        csgomarketSoScmSo = pd.DataFrame(columns=[u.ITEM_NAME, u.MARKETCSGO_PRICE_SO, u.STEAM_PRICE_SO_7D, u.STEAM_PRICE_SO_LAST, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D, u.PROFIT_NOW])
        csgomarketSoScmBo = pd.DataFrame(columns=[u.ITEM_NAME, u.MARKETCSGO_PRICE_SO, u.STEAM_PRICE_BO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT])

        scmSoCsgomarketSo = pd.DataFrame(columns=[u.ITEM_NAME, u.STEAM_PRICE_SO_7D, u.MARKETCSGO_PRICE_SO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D])
        scmBoCsgomarketSo = pd.DataFrame(columns=[u.ITEM_NAME, u.STEAM_PRICE_BO, u.MARKETCSGO_PRICE_SO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D, u.PROFIT])

        #csgomarketBuyOrdersDict = self.getDictCsgomarketBuyOrders(csgomarketBuyOrders)
        
        breakCont = 0
        cont = 0
        with alive_bar(len(csgomarketBuyOrders['items'])) as bar:
            for csgomarketItem in csgomarketBuyOrders['items']:
                try:
                    csgomarketItemName = csgomarketItem['market_hash_name']
                    csgomarketPrice = float(csgomarketItem['price'])
                    if not self.checkIsBannedItem(csgomarketItemName) and csgomarketPrice >= 1 and csgomarketPrice <= 5:
                        #csgomarketBuyOrder = csgomarketBuyOrdersDict[csgomarketItemName]
                        if checkSalesCsgomarket == True:
                            csgomarketVolume = self.getVolumeSalesMarketcsgo(csgomarketItemName)
                        else: csgomarketVolume = 0
                        
                        for steamItem in scmItems['data']:
                            if steamItem['market_hash_name'] == csgomarketItemName:
                                scmPrice7d = steamItem['prices']['safe_ts']['last_24h']
                                steamVolume = steamItem['prices']['sold']["avg_daily_volume"]

                                print(csgomarketItemName)
                                if isFast:
                                    singleItemData = 0
                                    highestBuyOrder = 0
                                    sellableSteamPrice = 0
                                else:
                                    if cont == 0: now = time.time()
                                    if cont == u.REQUEST_MINUTE: 
                                        later = time.time()
                                        print(now)
                                        print(later)
                                        timeSpent = math.ceil(later - now)
                                        waitTime = 60 - timeSpent
                                        print(str(u.REQUEST_MINUTE) + " REQUEST MADE IN " + str(timeSpent) +" SECONDS")

                                        if waitTime > 0:
                                            print("WAITING " + str(waitTime) + " SECONDS BEFORE MAKING MORE REQUESTS")
                                            time.sleep(waitTime)
                                        cont = 0

                                    singleItemData = CsgomarketApi().getScmData(csgomarketItemName)
                                    highestBuyOrder = singleItemData['histogram']['highest_buy_order']
                                    sellableSteamPrice = self.getSellableSteamPrice(singleItemData, steamVolume)
                                    cont = cont + 1

                                
                                try:
                                    cstoScmSoProfit7d = (scmPrice7d*0.88)/csgomarketPrice
                                except Exception as e:
                                    cstoScmSoProfit7d = 0
                                    #print("Failed item calculation ", e)
                                try:
                                    cstoScmSoProfitNow = (sellableSteamPrice*0.88)/csgomarketPrice
                                except Exception as e:
                                    cstoScmSoProfitNow = 0
                                    #print("Failed item calculation ", e)
                                newRowCstoScmSo = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                            u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                            u.STEAM_PRICE_SO_7D: [scmPrice7d],
                                                            u.STEAM_PRICE_SO_LAST: [sellableSteamPrice],
                                                            u.STEAM_VOLUME: [steamVolume],
                                                            u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                            u.PROFIT_7D: [cstoScmSoProfit7d],
                                                            u.PROFIT_NOW: [cstoScmSoProfitNow]
                                                            })
                                
                                try:
                                    cstoScmBoProfit = (highestBuyOrder*0.88)/csgomarketPrice
                                except Exception as e:
                                    cstoScmBoProfit = 0
                                    #print("Failed item calculation ", e)
                                newRowCstoScmBo = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                            u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                            u.STEAM_PRICE_BO: [highestBuyOrder],
                                                            u.STEAM_VOLUME: [steamVolume],
                                                            u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                            u.PROFIT: [cstoScmBoProfit],
                                                            })
                                
                                try: 
                                    scmSoToCsProfit7d = csgomarketPrice*0.95/scmPrice7d
                                except Exception as e:
                                    scmSoToCsProfit7d = 0
                                    #print("Failed item calculation ", e)
                                newRowScmSoToCs = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                            u.STEAM_PRICE_SO_7D: [scmPrice7d],
                                                            u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                            u.STEAM_VOLUME: [steamVolume],
                                                            u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                            u.PROFIT_7D: [scmSoToCsProfit7d],
                                                            })
                                
                                try:
                                    scmBoToCsProfit = csgomarketPrice*0.95/highestBuyOrder
                                except Exception as e:
                                    scmBoToCsProfit = 0
                                    #print("Failed item calculation ", e)
                                newRowScmBoToCs = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                            u.STEAM_PRICE_BO: [highestBuyOrder],
                                                            u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                            u.STEAM_VOLUME: [steamVolume],
                                                            u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                            u.PROFIT: [scmBoToCsProfit],
                                                            })
                                                            
                                csgomarketSoScmSo = pd.concat([csgomarketSoScmSo, newRowCstoScmSo])
                                csgomarketSoScmBo = pd.concat([csgomarketSoScmBo, newRowCstoScmBo])
                                scmSoCsgomarketSo = pd.concat([scmSoCsgomarketSo, newRowScmSoToCs])
                                scmBoCsgomarketSo = pd.concat([scmBoCsgomarketSo, newRowScmBoToCs])
                                break
                    #breakCont = breakCont + 1
                    #if breakCont > 40: break
                except Exception as e: print("Failed cheking an item, reason: ", e)
                bar()


        excelsDict = dict([
            ("csgomarketSO - scmSO", csgomarketSoScmSo),
            ("csgomarketSO - scmBO", csgomarketSoScmBo),
            ("scmSO - csgomarketSO", scmSoCsgomarketSo),
            ("scmBO - csgomarketSO", scmBoCsgomarketSo)
        ])

        return excelsDict
        
