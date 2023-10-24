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

    def add(self, stock_data):
        self.series.append(stock_data)

    def filter_date_range(self, start_date, end_date):
        """
        Filter the time series to only include stock data within a certain date range.

        :param start_date: The start date in 'YYYY-MM-DD' string format.
        :param end_date: The end date in 'YYYY-MM-DD' string format.
        :return: A list of Stock instances within the specified date range.
        """
        # Convert date strings to datetime objects for comparison
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter the series list to include only items within the specified range
        filtered_series = [data for data in self.series if start_date <= datetime.strptime(data.date, '%Y-%m-%d') <= end_date]
        
        return filtered_series

    

