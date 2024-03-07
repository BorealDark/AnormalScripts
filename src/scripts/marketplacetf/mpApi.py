import requests
from .utils import mpApiKey
from .utils import mpUtils


class MpApi:
    def getDashboardItems(key):
        parameters = {
            "key": mpApiKey.MP_API_KEY
        }
        head = {"User-Agent":"Mozilla/5.0"}
        
        response = requests.get(mpUtils.API_GETDASHBOARDITEMS_MP, params=parameters, headers=head).json()
        
        return response

    
        
  