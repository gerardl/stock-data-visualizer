import requests
# local imports
from Models import Stock, TimeSeries
from StockExceptions import StockQueryException

class StockService:
    def __init__(self, api_key):
        self.api_key = api_key

    def __query_api(self, data_type: str, symbol: str):
        url = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(data_type, symbol, self.api_key)
        
        # time series intraday requires an interval parameter
        if data_type == "TIME_SERIES_INTRADAY":
            url += "&interval=5min"
        # time series daily requires an outputsize parameter
        elif data_type == "TIME_SERIES_DAILY":
            url += "&outputsize=full"
        
        response = requests.get(url)
        # ensure the request was successful
        if response.status_code != 200:
            raise StockQueryException("API returned an http error. Add detail to this message?")
        # check for json errors / no response?
        if 'Error Message' in response.text:
            raise StockQueryException("API was accessible but returned an error message. Did you enter a valid stock symbol?")
        return response.json()

    def __create_time_series(self, symbol: str, json_response, items_label: str) -> TimeSeries:
        """
        Create a TimeSeries instance from the JSON response from the API.
        """
        try:
            time_series = TimeSeries(symbol)
            for date, daily_data in json_response[items_label].items():
                stock_data = Stock(
                    symbol=symbol,
                    date=date,
                    open=float(daily_data['1. open']),
                    high=float(daily_data['2. high']),
                    low=float(daily_data['3. low']),
                    close=float(daily_data['4. close']),
                    volume=int(daily_data['5. volume']),
                )
                time_series.add(stock_data)

            return time_series
        except KeyError:
            raise StockQueryException("API returned an unexpected response.")

    def get_intraday(self, symbol: str) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_INTRADAY", symbol)
        time_series = self.__create_time_series(symbol, res, 'Time Series (5min)')
        return time_series
        
    def get_daily(self, symbol: str) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_DAILY", symbol)
        time_series = self.__create_time_series(symbol, res, 'Time Series (Daily)')
        return time_series
    
    def get_weekly(self, symbol: str) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_WEEKLY", symbol)
        time_series = self.__create_time_series(symbol, res, 'Weekly Time Series')
        return time_series
    
    def get_monthly(self, symbol: str) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_MONTHLY", symbol)
        time_series = self.__create_time_series(symbol, res, 'Monthly Time Series')
        return time_series
