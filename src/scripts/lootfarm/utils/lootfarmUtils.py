URI_LOOTFARM_RUST = "https://loot.farm/fullpriceRUST.json"
URI_LOOTFARM_TF = "https://loot.farm/fullpriceTF2.json"

URI_STEAMAPI_SCM = "https://api.steamapis.com/market/items/"

QUERY = "query"
START = "start"
COUNT = "count"
NORENDER = "norender"
RUST_APPID_SCM = "appid:252490"
API_SCMRENDER_STEAM = "https://steamcommunity.com/market/search/render/"
RESULTS = "results"
HASH_NAME = "hash_name"
SELL_PRICE = "sell_price"
NAME = "name"
STEAM_PRICE = "steam_price"
LOOTFARM_PRICE = "lootfarm_price"
PROFIT = "profit"
LOOTFARM_QUANTITY = "lootfarm_quantity"
STEAM_SALES_QUANTITY = "steam_sales_quantity"
VOLUME = "volume"
ITEM_NAME = "item_name"
QUANTITY = "quantity"
APPID = "appid"
RUST_APPID = "252490"
CURRENCY = "currency"
STEAM_EURO_CURRENCY = 3
MARKET_HASH_NAME = "market_hash_name"
API_PRICEOVERVIEW_STEAM = "https://steamcommunity.com/market/priceoverview/"
MINIMUM_VOLUME = 5.0
MP_FEE = 0.9
STEAM_FEE = 0.88
RATE = "rate"
LOOTFARM_VALUE = 'lootfarm_value'
STOCK_TO_SELL = 'stock_to_sell'
SCM_BALANCE_RATE = 'scm_bal_rate'


def getCurrency(rates, currency):
    for index, row in rates.iterrows():
        if row["Currency Name"] == currency:
            return row["Price"]

######################
#VALORES MODIFICABLES#
######################
KEY_PRICE_USD = 1.68
KEY_PRICE_LOOTFARM = 2.50

MINIMUM_TF_PRICE = 0
MINIMUM_RUST_PRICE = 0
MINIMUM_DAILY_SALES_SCM = 0





