import requests
from datetime import datetime
# local imports
from Models import Stock, TimeSeries
from Utility import Utility
from StockExceptions import StockQueryException, StockQueryLimitException, StockEndpointException

class StockService:
    BASE_URL = "https://www.alphavantage.co/query"
    INTRA_TYPE = "TIME_SERIES_INTRADAY"
    DAILY_TYPE = "TIME_SERIES_DAILY"
    WEEKLY_TYPE = "TIME_SERIES_WEEKLY"
    MONTHLY_TYPE = "TIME_SERIES_MONTHLY"

    def __init__(self, api_key):
        self.api_key = api_key

    def __query_api(self, data_type: str, symbol: str, additional_params: dict = {}):
        params = {
            "function": data_type,
            "symbol": symbol,
            "apikey": self.api_key
        }
        params.update(additional_params)

        response = requests.get(self.BASE_URL, params=params)
        # ensure the request was successful
        if response.status_code != 200:
            raise StockEndpointException("API returned an http error. Add detail to this message?")
        # check for json errors / no response?
        if 'Error Message' in response.text:
            raise StockQueryException("API was accessible but returned an error message. Did you enter a valid stock symbol?")
        # check for api limit reached
        if 'Thank you for using' in response.text:
            raise StockQueryLimitException()
        return response.json()

    def __create_series_data(self, symbol: str, json_response, items_label: str) -> [Stock]:
        """
        Create a TimeSeries instance from the JSON response from the API.
        """
        try:
            series_data = []
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
                series_data.append(stock_data)

            return series_data
        except KeyError:
            raise StockQueryException("API returned an unexpected response.")

    # Intraday is limited to a 1 month range, so we need to make multiple requests to get the full dataset
    def get_intraday(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        months = Utility.get_months_between(start_date, end_date)
        series_data = []
        for month in months:
            # TODO: decide what interval we want to use for intraday
            res = self.__query_api(self.INTRA_TYPE, symbol, {"outputsize": "full", "month": month.strftime('%Y-%m'), "interval": "60min"})
            series_data += self.__create_series_data(symbol, res, 'Time Series (60min)')

        return TimeSeries(symbol, self.INTRA_TYPE, start_date, end_date, series_data)

    def get_daily(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api(self.DAILY_TYPE, symbol, {"outputsize": "full"})
        series_data = self.__create_series_data(symbol, res, 'Time Series (Daily)')
        return TimeSeries(symbol, self.DAILY_TYPE, start_date, end_date, series_data)
    
    def get_weekly(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api(self.WEEKLY_TYPE, symbol)
        series_data = self.__create_series_data(symbol, res, 'Weekly Time Series')
        return TimeSeries(symbol, self.WEEKLY_TYPE, start_date, end_date, series_data)
    
    def get_monthly(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api(self.MONTHLY_TYPE, symbol)
        series_data = self.__create_series_data(symbol, res, 'Monthly Time Series')
        return TimeSeries(symbol, self.MONTHLY_TYPE, start_date, end_date, series_data)
