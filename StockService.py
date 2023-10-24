import requests

class StockService:
    def __init__(self, api_key):
        self.api_key = api_key

    def __query_api(self, data_type, symbol):
        url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(data_type, symbol, self.api_key)
        response = requests.get(url)
        return response.json()

    def get_intraday_data(self, symbol):
        return self.__query_api("TIME_SERIES_INTRADAY", symbol)

    def get_daily_data(self, symbol):
        return self.__query_api("TIME_SERIES_DAILY", symbol)
    
    def get_weekly_data(self, symbol):
        return self.__query_api("TIME_SERIES_WEEKLY", symbol)
    
    def get_monthly_data(self, symbol):
        return self.__query_api("TIME_SERIES_MONTHLY", symbol)
