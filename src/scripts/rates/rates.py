import requests
from .utils import ratesUtils as u

class RatesService:
    
    def getCurrencyToCurrency(self, currency1, currency2):
        url = u.buildEndpointRates(currency1, currency2)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud a la API: {response.status_code}. Verifica tu API key o la conexión.")
        return response.json().get("conversion_rate")
    
    def getUsdtoEur(self):
        usdToEur = self.getCurrencyToCurrency(u.USD, u.EUR)
        print("USD TO EURO RATIO =", usdToEur)
        return usdToEur


