import pandas as pd
from .utils import backpackUtils as u
from .backpacktfApi import BackpacktfApi
import time
from alive_progress import alive_bar
import math

class BackpacktfService:

    # GET BACKPACK ITEM SNAPSHOT
    def getBackpackSnapshot(self, itemName):
        time.sleep(1)
        return BackpacktfApi().getBackpackSnapshot(itemName)
        


    # PROCESS THE SNAPSHOT AND CREATES A LIST WITH THE PRICES
    def processSnapshot(self, snapshot):
        itemData = {}
        for listing in snapshot['listings']:
            #print(listing['steamid'])
            hasAttributes = False
            isBot = False
            isGladiatorBot = False
            intent = listing['intent']

            if intent == 'buy':            
                try:
                    attributtes = listing['item']['attributes']
                    for attributte in attributtes:
                        if attributte['defindex'] == "1009":
                            hasAttributes = True
                except:
                    #print("NO ATRIBUTESSSSSS")
                    hasAttributes = False

            if hasAttributes is False:
                try:
                    if listing['buyout'] == 1:
                        botInfo = listing['userAgent']
                        isBot = True
                        if "Gladiator.tf" in botInfo['client']:
                            isGladiatorBot = True
                except: isBot = False

                for bannedBot in u.NOT_CHECK_THESE_BOTS:
                    if listing['steamid'] == bannedBot: 
                        isBot = False
                        break

                if isBot:
                    priceKeys = 0
                    priceRef = 0
                    try: priceKeys = listing['currencies']['keys']
                    except: None
                    try: priceRef = listing['currencies']['metal']
                    except: None
                    itemDataPrice = {
                        'intent': intent,
                        'pricekeys': priceKeys,
                        'priceref': priceRef,
                        'isgladiatorbot': isGladiatorBot
                    }
                    itemData[str(listing['steamid'])+'_'+intent] = itemDataPrice
        #print(itemData)
        return itemData

    ### SCM FUNCTIONS ###
    def getScmItemsVolume(self, scmItems, minVolume):
        scmItemsVolume = pd.DataFrame(columns=[u.SCM_NAME,u.SCM_PRICE, u.AVG_SOLD])
        for item in scmItems['data']:
            itemName = item['market_hash_name']
            
            try: itemPrice = item['prices']['safe_ts']['last_24h']
            except:
                try: itemPrice = item['prices']['safe_ts']['last_7d']
                except: itemPrice = 0

            try: itemVolume = item['prices']['sold']['last_24h']
            except: 
                try: itemVolume = item['prices']['sold']['avg_daily_volume']
                except: itemVolume = 0
            
            if itemVolume >= minVolume and itemPrice > 0.08:
                newRow = pd.DataFrame({u.SCM_NAME: [itemName],
                                        u.SCM_PRICE: [itemPrice], 
                                        u.AVG_SOLD: [itemVolume],
                                        })

                scmItemsVolume = pd.concat([scmItemsVolume, newRow])
        
        scmItemsVolume = scmItemsVolume.sort_values(by=[u.AVG_SOLD], ascending=False)
        return scmItemsVolume

    
    def processScmItemsForBot(self, scmitems):
        scmItemsProcessed = pd.DataFrame(columns=[u.SCM_NAME,u.SCM_PRICE, u.AVG_SOLD])
        
        for index, row in scmitems.iterrows():
            itemName = row[u.SCM_NAME]
            itemPrice = row[u.SCM_PRICE]
            itemVolume = row[u.AVG_SOLD]
            #print(itemName)
            isGoodItem = True
            if "(" in itemName:
                isGoodItem = False
            if isGoodItem and "Kit" in itemName:
                isGoodItem = False
            if isGoodItem and "Unusual" in itemName:
                isGoodItem = False
            if isGoodItem and "Strangifier" in itemName:
                isGoodItem = False
            if itemPrice < 0.50:
                isGoodItem = False
            
            if isGoodItem:
                newRow = pd.DataFrame({u.SCM_NAME: [itemName],
                                        u.SCM_PRICE: [itemPrice], 
                                        u.AVG_SOLD: [itemVolume],
                                        })

                scmItemsProcessed = pd.concat([scmItemsProcessed, newRow])
        
        return scmItemsProcessed

    
    
    def getScmProfitableItems(self, scmItems, rateUSDEUR, isBuyOrder):
        cont = 0
        profitableScmProfitableItems = pd.DataFrame(columns=[u.SCM_NAME,u.SCM_PRICE, u.BP_PRICE, u.SCM_PROFIT, u.AVG_SOLD])

        scmItemsVolume = self.getScmItemsVolume(scmItems, 3)
        print(scmItemsVolume)
        scmItemsProcessed = self.processScmItemsForBot(scmItemsVolume)
        print(scmItemsProcessed)
        keyPrice = self.getKeyPrice()
        
        print("KEY PRICE = " +str(keyPrice))

        loops = int(len(scmItemsProcessed))
        with alive_bar(loops) as bar:
            for index, row in scmItemsProcessed.iterrows():
                try:
                    itemName = row[u.SCM_NAME]
                    scmPrice = round(row[u.SCM_PRICE], 2)
                    avgSold = row[u.AVG_SOLD]

                    checkItem = False
                    if "#" not in itemName and "Case" not in itemName and "Key" not in itemName:
                        if isBuyOrder: checkItem = True
                        else:
                            if scmPrice >= 1: checkItem = True

                    if checkItem:
                        BpPrice = 0
                        if isBuyOrder:
                            snapshot = self.getBackpackSnapshot(itemName)
                            itemPrices = self.processSnapshot(snapshot)
                            BpPrice = self.getBpBuyPrice(itemPrices, False, keyPrice, True)
                        else:
                            BpPrice = self.getSellPrice(itemName, keyPrice)

                        print (itemName + " PRICE = "+str(BpPrice)+" keys")

                        """
                        for listing in itemPrices:
                            #print(itemPrices[listing])
                            if itemPrices[listing]['intent'] == "buy":
                                if not priceFound:
                                    BpPrice = itemPrices[listing]['pricekeys'] + itemPrices[listing]['priceref']/63
                                    priceFound = True
                                if itemPrices[listing]['isgladiatorbot'] == True: 
                                    print(itemName)
                                    print(itemPrices[listing]['pricekeys'])
                                    print(itemPrices[listing]['priceref']/63)
                                    BpPrice = itemPrices[listing]['pricekeys'] + itemPrices[listing]['priceref']/63
                                    break
                        """
                        if BpPrice != 0:
                            if scmPrice <= 0.21:
                                profit = ((((((scmPrice-0.02)/2.35)*2.49)*0.90)/1.51))/BpPrice
                            else:
                                profit = ((((((scmPrice/1.15)/2.35)*2.49)*0.90)/1.51))/BpPrice
                        else: profit = 0

                            
                        #print(itemName)
                        #print(itemPrices)
                        #cont = cont + 1
                        #print(cont)
                        #if cont > 50: break

                        newRow = pd.DataFrame({u.SCM_NAME: [itemName],
                                                u.SCM_PRICE: [scmPrice], 
                                                u.BP_PRICE: [BpPrice],
                                                u.SCM_PROFIT: [profit],
                                                u.AVG_SOLD: [avgSold],
                                                })
                        
                        profitableScmProfitableItems = pd.concat([profitableScmProfitableItems, newRow])
                except Exception as e: 
                    print("Failed checking item "+itemName, e)
                bar()        

            profitableScmProfitableItems = profitableScmProfitableItems.sort_values(by=[u.SCM_PROFIT], ascending=False)
            return profitableScmProfitableItems
    
    # GET PRICES FUNCTIONS
    def getBpBuyPrice(self, itemPrices, onlyRef, keyRef, onlyGlad):
        priceFound = False
        BpPrice = 0
        for listing in itemPrices:
                    #print(itemPrices[listing])
                    if itemPrices[listing]['intent'] == "buy":
                        if not priceFound:
                            if onlyRef: 
                                BpPrice = itemPrices[listing]['priceref']
                            else:
                                BpPrice = itemPrices[listing]['pricekeys'] + itemPrices[listing]['priceref']/keyRef
                            priceFound = True
                            if not onlyGlad: return BpPrice
                        if itemPrices[listing]['isgladiatorbot'] == True: 
                            if onlyRef: 
                                itemPrices[listing]['priceref']
                            else:
                                BpPrice = itemPrices[listing]['pricekeys'] + itemPrices[listing]['priceref']/keyRef
                            #print("BP PRICE = "+str(BpPrice))
                            return BpPrice
        return BpPrice
    
    def getBpSellPrice(self, itemPrices, keyRef):
        BpPrice = 0
        for listing in itemPrices:
                    #print(itemPrices[listing])
                    if itemPrices[listing]['intent'] == "sell":                            
                                BpPrice = itemPrices[listing]['pricekeys'] + itemPrices[listing]['priceref']/keyRef
                                return BpPrice
        return BpPrice
                            
    def getKeyPrice(self):
        snapshotKey = self.getBackpackSnapshot(u.KEY)
        keyPrices = self.processSnapshot(snapshotKey)
        keyPrice = self.getBpBuyPrice(keyPrices, True, None, False)
        return keyPrice

    def getSellPrice(self, itemName, keyRef):
        snapshot = self.getBackpackSnapshot(itemName)
        itemPrices = self.processSnapshot(snapshot)
        itemSellPrice = self.getBpSellPrice(itemPrices, keyRef)
        return itemSellPrice
    

    def getBackpackToLootfarm(self, tf2LootfarmItems):
        backpackToLootfarm = pd.DataFrame(columns=[u.NAME,u.BACKPACK_PRICE, u.LOOTFARM_PRICE, u.VALUE, u.STOCK_TO_SELL])
        keyRef = self.getKeyPrice()
        with alive_bar(len(tf2LootfarmItems)) as bar:
            for item in tf2LootfarmItems:
                itemName = item['name']
                print(itemName)
                stockToSell = item['max'] - item['have']
                lootfarmPrice = math.floor(item['price']/1.03)/100
                cont = 0
                print(lootfarmPrice)
                print(stockToSell)
                if lootfarmPrice >= 1 and stockToSell > 0 and "Unusual" not in itemName:
                    try:
                        itemSellPrice = self.getSellPrice(itemName, keyRef)
                        print("Item = " + str(itemName) + " sell order price = " + str(itemSellPrice))
                        value = lootfarmPrice/itemSellPrice
                        newRow = pd.DataFrame({u.NAME: [itemName],
                                        u.BACKPACK_PRICE: [itemSellPrice], 
                                        u.LOOTFARM_PRICE: [lootfarmPrice],
                                        u.VALUE: [value],
                                        u.STOCK_TO_SELL: [stockToSell],
                                        })
                        backpackToLootfarm = pd.concat([backpackToLootfarm, newRow])
                        if cont > 50: break

                    except Exception as e:
                        print ("Failed checking item " + itemName, e)
                cont = cont + 1
                bar()
        return backpackToLootfarm
    
    def getBackpackToCstrade(self, tf2LootfarmItems):
        backpackToCstrade = pd.DataFrame(columns=[u.NAME,u.BACKPACK_PRICE, u.CSTRADE_PRICE, u.VALUE, u.STOCK_TO_SELL])
        keyRef = self.getKeyPrice()
        with alive_bar(len(tf2LootfarmItems)) as bar:
            for itemName in tf2LootfarmItems:
                print(itemName)
                stockToSell = tf2LootfarmItems[itemName]['can_take']
                cstradePrice = math.floor(tf2LootfarmItems[itemName]['price']/1.07)
                cont = 0
                print(cstradePrice)
                print(stockToSell)
                if cstradePrice >= 1 and stockToSell > 0 and "Unusual" not in itemName:
                    try:
                        itemSellPrice = self.getSellPrice(itemName, keyRef)
                        print("Item = " + str(itemName) + " sell order price = " + str(itemSellPrice))
                        value = cstradePrice/itemSellPrice
                        newRow = pd.DataFrame({u.NAME: [itemName],
                                        u.BACKPACK_PRICE: [itemSellPrice], 
                                        u.CSTRADE_PRICE: [cstradePrice],
                                        u.VALUE: [value],
                                        u.STOCK_TO_SELL: [stockToSell],
                                        })
                        backpackToCstrade = pd.concat([backpackToCstrade, newRow])

                    except Exception as e:
                        print ("Failed checking item " + itemName, e)

                bar()
        return backpackToCstrade
    
    def getBackpackPricesMp(self, mpItems):
        keyPrice = self.getBpBuyPrice(self.processSnapshot(self.getBackpackSnapshot(u.KEY)), True, None, False)
        print("KEY PRICE = "+ str(keyPrice))
        
        mpItemsAux = mpItems
        print (mpItemsAux)
        cont = 0
        for mpItemName in mpItemsAux['NAME']:
            if "steam" not in mpItemsAux["SKU"][cont]:
                try:
                    print (mpItemName)
                    snapshot = self.getBackpackSnapshot(mpItemName)
                    processedSnapshot = self.processSnapshot(snapshot) 
                    price = self.getBpBuyPrice(processedSnapshot, False, keyPrice, False)
                    print(price)
                    mpItemsAux[u.BACKPACK_PRICE_BUY][cont] = price

                    price_so = self.getBpSellPrice(processedSnapshot, keyPrice)
                    mpItemsAux[u.BACKPACK_PRICE_SELL][cont] = price_so

                    print("ITEM "+ mpItemName + " PRICE = " + str(mpItemsAux[u.BACKPACK_PRICE_BUY][cont]))
                #DEBUG
                except Exception as e:
                        try:
                            snapshot = self.getBackpackSnapshot("The "+mpItemName)
                            processedSnapshot = self.processSnapshot(snapshot) 
                            price = self.getBpBuyPrice(processedSnapshot, False, keyPrice, False)
                            print(price)
                            mpItemsAux[u.BACKPACK_PRICE_BUY][cont] = price

                            price_so = self.getBpSellPrice(processedSnapshot, keyPrice)
                            mpItemsAux[u.BACKPACK_PRICE_SELL][cont] = price_so

                            print("ITEM "+ mpItemName + " PRICE = " + str(mpItemsAux[u.BACKPACK_PRICE_BUY][cont]))
                        
                        except:
                            print("ITEM " + mpItemName + " NOT FOUND", e)

            if mpItemsAux[u.BACKPACK_PRICE_BUY][cont] > 0:
                mpItemsAux[u.PROFIT][cont] = ((mpItemsAux[u.MARKETPLACE_PRICE][cont]*0.9)/u.KEY_PRICE_USD)/mpItemsAux[u.BACKPACK_PRICE_BUY][cont]
            cont = cont + 1
            #if cont > 30: break
        return mpItemsAux

            