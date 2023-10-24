import requests
import json
from StockExceptions import StockQueryException

class StockService:
    def __init__(self, api_key):
        self.api_key = api_key

    def __query_api(self, data_type, symbol):
        url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(data_type, symbol, self.api_key)
        response = requests.get(url)
        # ensure the request was successful
        if response.status_code != 200:
            raise StockQueryException("TODO: Add useful message here")
        # parse the response as JSON
        json_response = response.json()
        # check for json errors / no response?
        return response.json()

    def get_intraday_data(self, symbol, start_date, end_date):
        res = self.__query_api("TIME_SERIES_INTRADAY", symbol)
        # filter the data by date
        return res
        
    def get_daily_data(self, symbol):
        res = self.__query_api("TIME_SERIES_DAILY", symbol)
        return res
    
    def get_weekly_data(self, symbol):
        return self.__query_api("TIME_SERIES_WEEKLY", symbol)
    
    def get_monthly_data(self, symbol):
        return self.__query_api("TIME_SERIES_MONTHLY", symbol)
