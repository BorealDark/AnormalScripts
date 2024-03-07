import pandas as pd

class DataManegerService:
    def excelToData(self, path, sheetName):
        data = pd.read_excel(path, sheet_name=str(sheetName))
        return data

    def dataToExcel(self, path, sheetName, data):
        data.to_excel(path, sheet_name=str(sheetName), index=False)

