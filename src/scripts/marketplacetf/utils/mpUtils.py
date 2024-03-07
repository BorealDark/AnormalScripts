API_GETDASHBOARDITEMS_MP = "https://marketplace.tf/api/Seller/GetDashboardItems/v2"
API_GETSALES_MP = "https://marketplace.tf/api/Seller/GetSales/v2"

TF2_QUALITIES = {"Unique", "Strange", "Genuine", "Vintage", "Uncraftable", "Kits", "Unusualifier", "Festivized"}

KS = "ks-"
KE = "ke-"
P = "p"

SKU = "SKU"
BACKPACK_URL = "BACKPACK URL"
MARKETPLACE_URL = "MARKETPLACE URL"
ADD_GLADIATOR = "ADD GLADIATOR"
NAME = "NAME"

GLADIATOR_BACKPACK_URI = "https://gladiator.tf/bp/"
GLADIATOR_BACKPACK__NON_CRAFTABLE_URI = "https://gladiator.tf/bp/Non-Craftable%20"

MARKETPLACE_URI = "https://marketplace.tf/items/tf2/"
GLADIATOR_URI = "https://gladiator.tf/manage/5fd2945004d4bc0c12fc1399/item/"
GLADIATOR_URI_NON_CRAFTABLE = "https://gladiator.tf/manage/5fd2945004d4bc0c12fc1399/item/Non-Craftable%20"

ADD_URL = "/add"
BACKPACK_URI_START = "https://backpack.tf/stats/"
BACKPACK_URI_CRAFTABLE = "/Tradable/Craftable"
BACKPACK_URI_UNCRAFTABLE = "/Tradable/Non-Craftable"

UNCRAFTABLE = "Uncraftable"
UNIQUE = "Unique"

ITEMS = "items"
SKU = "sku"
BIG_SKU = "SKU"
QUANTITY = "QUANTITY"
NUM_FOR_SALE = "num_for_sale"
BP_PRICE = "BP PRICE"
BUY_HALF_SCRAP = "buyHalfScrap"
BUY_KEYS = "buyKeys"

STOCK = "STOCK"
HOW_MANY_BUY = "HOW MANY BUY"

ADD_BOT = "ADD BOT"

FINISHED_ITEMS = "Finished the items "

MP_URL = "MP URL"
BACKPACK_PRICE_BUY = "BACKPACK PRICE BUY ORDER"
BACKPACK_PRICE_SELL = "BACKPACK PRICE SELL ORDER"

MARKETPLACE_PRICE = "MARKETPLACE PRICE"
PROFIT = "PROFIT"
PRICE = "price"


#MP SALES CONTROLLER
HIGHEST_TIME = "HIGHEST_TIME"
TIME = "time"
SALES =  "sales"
PAID = "paid"

#
SHEENS = {"Agonizing Emerald", "Deadly Daffodil", "Hot Rod", "Manndarin", "Mean Green", "Team Shine", "Villainous Violet"}
EFFECTS = {"Cerebral Discharge", "Fire Horns", "Flames", "Hypno-Beam", "Incinerator", "Singularity", "Tornado"}






def filterItem(itemToBeFiltered):
        filteredItemDivided = itemToBeFiltered.split(";")
        itemFiltered = ""
        f = False
        for div in filteredItemDivided:
            if(KS not in div and P not in div and KE not in div and not f):
                itemFiltered = itemFiltered+div
            elif(KS not in div and P not in div and KE not in div and f):
                itemFiltered = itemFiltered+';'+div
            f = True

        return itemFiltered

def convertPrice(buyHalfScrap, buyKeys, keyref):
    priceREF = buyHalfScrap/18
    priceKEYS = (priceREF/keyref)+buyKeys
    return priceKEYS

#ONLY USED IF YOU USE PRICES.TF TO CHECK NON PROFITABLE ITEMS (NOT RECOMENDED)
KEYPRICEUSD = 1.55
