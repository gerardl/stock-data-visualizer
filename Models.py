from datetime import datetime

class Stock:
    def __init__(self, symbol, date, open, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

class TimeSeries:
    def __init__(self, symbol):
        self.symbol = symbol
        self.series = []

    def __init__(self, symbol: str, series_type: str, start_date: datetime, end_date: datetime, series: list):
        self.symbol = symbol
        self.series_type = series_type
        self.start_date = start_date
        self.end_date = end_date
        self.series = self.__filter_date_range(series)

    def __str_to_datetime(self, date_str: str) -> datetime:
        try:
            # Try to parse string as datetime
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # If parsing as datetime fails, try parsing as date
            return datetime.strptime(date_str, '%Y-%m-%d')

    def __filter_date_range(self, series: list):
        """
        Filter the time series to only include stock data within the specified date range.
        :return: A list of Stock instances within the specified date range.
        """
        filtered_series = [data for data in series if self.start_date <= self.__str_to_datetime(data.date) <= self.end_date]
        return filtered_series

    

