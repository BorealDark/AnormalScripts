from .csgomarketApi import CsgomarketApi
from .utils import csgomarketUtils as u
import pandas as pd
from datetime import datetime
from alive_progress import alive_bar


class CsgomarketService:
    def getAllItems(self, str):
        return CsgomarketApi().getAllItems(str)
        
    
    def getSellableSteamPrice(self, singleItemData):
        return 0

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


    def csgomarketScmDataProcesor(self, csgomarketData, csgomarketBuyOrders, scmItems):
        csgomarketSoScmSo = pd.DataFrame(columns=[u.ITEM_NAME, u.MARKETCSGO_PRICE_SO, u.STEAM_PRICE_SO_7D, u.STEAM_PRICE_SO_LAST, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D, u.PROFIT_NOW])
        csgomarketSoScmBo = pd.DataFrame(columns=[u.ITEM_NAME, u.MARKETCSGO_PRICE_SO, u.STEAM_PRICE_BO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT])

        scmSoCsgomarketSo = pd.DataFrame(columns=[u.ITEM_NAME, u.STEAM_PRICE_SO_7D, u.MARKETCSGO_PRICE_SO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D])
        scmBoCsgomarketSo = pd.DataFrame(columns=[u.ITEM_NAME, u.STEAM_PRICE_BO, u.MARKETCSGO_PRICE_SO, u.STEAM_VOLUME, u.CSGOMARKET_VOLUME, u.PROFIT_7D, u.PROFIT])

        #csgomarketBuyOrdersDict = self.getDictCsgomarketBuyOrders(csgomarketBuyOrders)
        
        breakCont = 0
        with alive_bar(len(csgomarketData['items'])) as bar:
            for csgomarketItem in csgomarketData['items']:
                csgomarketItemName = csgomarketItem['market_hash_name']
                csgomarketPrice = float(csgomarketItem['price'])
                if not self.checkIsBannedItem(csgomarketItemName) and csgomarketPrice >= 1 and csgomarketPrice <= 1000:
                    #csgomarketBuyOrder = csgomarketBuyOrdersDict[csgomarketItemName]
                    csgomarketVolume = self.getVolumeSalesMarketcsgo(csgomarketItemName)
                    
                    for steamItem in scmItems['data']:
                        if steamItem['market_hash_name'] == csgomarketItemName:
                            scmPrice7d = steamItem['prices']['safe_ts']['last_7d']
                            steamVolume = steamItem['prices']['sold']['last_24h']

                            singleItemData = CsgomarketApi().getScmData(csgomarketItemName)

                            highestBuyOrder = singleItemData['histogram']['highest_buy_order']
                            sellableSteamPrice = self.getSellableSteamPrice(singleItemData)
                            
                            cstoScmSoProfit7d = (scmPrice7d*0.88)/csgomarketPrice
                            cstoScmSoProfitNow = (sellableSteamPrice*0.88)/csgomarketPrice
                            newRowCstoScmSo = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                        u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                        u.STEAM_PRICE_SO_7D: [scmPrice7d],
                                                        u.STEAM_PRICE_SO_LAST: [sellableSteamPrice],
                                                        u.STEAM_VOLUME: [steamVolume],
                                                        u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                        u.PROFIT_7D: [cstoScmSoProfit7d],
                                                        u.PROFIT_NOW: [cstoScmSoProfitNow]
                                                        })
                            
                            cstoScmBoProfit = (highestBuyOrder*0.88)/csgomarketPrice
                            newRowCstoScmBo = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                        u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                        u.STEAM_PRICE_BO: [highestBuyOrder],
                                                        u.STEAM_VOLUME: [steamVolume],
                                                        u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                        u.PROFIT: [cstoScmBoProfit],
                                                        })
                            
                            scmSoToCsProfit7d = csgomarketPrice*0.95/scmPrice7d
                            newRowScmSoToCs = pd.DataFrame({u.ITEM_NAME: [csgomarketItemName], 
                                                        u.STEAM_PRICE_SO_7D: [scmPrice7d],
                                                        u.MARKETCSGO_PRICE_SO: [csgomarketPrice],
                                                        u.STEAM_VOLUME: [steamVolume],
                                                        u.CSGOMARKET_VOLUME: [csgomarketVolume],
                                                        u.PROFIT_7D: [scmSoToCsProfit7d],
                                                        })
                            
                            scmBoToCsProfit = csgomarketPrice*0.95/highestBuyOrder
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
                breakCont = breakCont + 1
                if breakCont > 40: break
                bar()


        excelsDict = dict([
            ("csgomarketSO - scmSO", csgomarketSoScmSo),
            ("csgomarketSO - scmBO", csgomarketSoScmBo),
            ("scmSO - csgomarketSO", scmSoCsgomarketSo),
            ("scmBO - csgomarketSO", scmBoCsgomarketSo)
        ])

        return excelsDict
        
