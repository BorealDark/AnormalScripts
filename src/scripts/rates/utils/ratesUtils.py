from .ratesApikey import RATES_APIKEY
ENDPOINT_RATES = f"https://v6.exchangerate-api.com/v6/{RATES_APIKEY}/pair/"
EUR = "EUR"
USD = "USD"

def buildEndpointRates(currency1, currency2):
    return f"{ENDPOINT_RATES}{currency1}/{currency2}"
    