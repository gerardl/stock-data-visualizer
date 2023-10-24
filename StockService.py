import requests
from datetime import datetime
# local imports
from Models import Stock, TimeSeries
from StockExceptions import StockQueryException, StockQueryLimitException, StockEndpointException

class StockService:
    BASE_URL = "https://www.alphavantage.co/query"

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
        if 'Note' in response.text:
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

    def __get_months_between(self, start_date: datetime, end_date: datetime):
        """
        Get all the months between the start date and end date.

        :param start_date: The start date as a datetime object.
        :param end_date: The end date as a datetime object.
        :return: A list of the first day of each month between the start and end dates, inclusive.
        """
        # Ensure the start_date is less than or equal to the end_date
        if start_date > end_date:
            raise ValueError("The start date must be before or the same as the end date")

        months = []
        # Current date to keep track of the month currently being processed
        current_date = start_date.replace(day=1)  # We set the day to 1 to ensure we always start from the first day of the month

        while current_date <= end_date:
            months.append(current_date)
            # Move to the next month. The "%Y-%m-%d" format ensures we are working with the first day of each month.
            next_month = current_date.month + 1 if current_date.month < 12 else 1
            next_year = current_date.year if current_date.month < 12 else current_date.year + 1
            current_date = current_date.replace(month=next_month, year=next_year)

        return months
    
    # Intraday is limited to a 1 month range, so we need to make multiple requests to get the full dataset
    def get_intraday(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        months = self.__get_months_between(start_date, end_date)
        series_data = []
        for month in months:
            res = self.__query_api("TIME_SERIES_INTRADAY", symbol, {"outputsize": "full", "month": month.strftime('%Y-%m'), "interval": "60min"})
            series_data += self.__create_series_data(symbol, res, 'Time Series (60min)')

        return TimeSeries(symbol, "TIME_SERIES_INTRADAY", start_date, end_date, series_data)

    def get_daily(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_DAILY", symbol, {"outputsize": "full"})
        series_data = self.__create_series_data(symbol, res, 'Time Series (Daily)')
        return TimeSeries(symbol, "TIME_SERIES_DAILY", start_date, end_date, series_data)
    
    def get_weekly(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_WEEKLY", symbol)
        series_data = self.__create_series_data(symbol, res, 'Weekly Time Series')
        return TimeSeries(symbol, "TIME_SERIES_WEEKLY", start_date, end_date, series_data)
    
    def get_monthly(self, symbol: str, start_date: datetime, end_date: datetime) -> TimeSeries:
        res = self.__query_api("TIME_SERIES_MONTHLY", symbol)
        series_data = self.__create_series_data(symbol, res, 'Monthly Time Series')
        return TimeSeries(symbol, "TIME_SERIES_MONTHLY", start_date, end_date, series_data)
