import pygal
from datetime import datetime, timedelta
import lxml
from Utility import Utility
from Models import Stock, TimeSeries

class StockChart:
    def graphData(self, chartType, time_series: TimeSeries):
        chart = pygal.Line(x_label_rotation=35) if chartType == 2 else pygal.Bar(x_label_rotation=35)
        chart.title = f'Stock Data for {time_series.symbol}: {time_series.start_date} to {time_series.end_date}'
        time_series.series.reverse()
        chart.x_labels = [stock.date for stock in time_series.series]
        
        # use time_series.sersies for pygal chart
        open = [item.open for item in time_series.series]
        high = [item.high for item in time_series.series]
        low = [item.low for item in time_series.series]
        close = [item.close for item in time_series.series]
        chart.add('Open', open)
        chart.add('High', high)
        chart.add('Low', low)
        chart.add('Close', close)
        
        # show in browser with lxml
        chart.render_in_browser()





