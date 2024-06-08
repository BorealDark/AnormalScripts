import pandas as pd

class DataManegerService:
    def excelToData(self, path, sheetName):
        data = pd.read_excel(path, sheet_name=str(sheetName))
        return data

    def dataToExcel(self, path, sheetName, data):
        cont = 0
        while(cont < 100):
            try: 
                data.to_excel(path, sheet_name=str(sheetName), index=False)
                break
            except Exception as e:
                print("Failed saving the excel, waiting 10 seconds before trying again...", e)
            cont = cont + 1

