import pygal
from datetime import datetime, timedelta
import lxml
from Utility import Utility
from Models import Stock, TimeSeries

class StockChart:
    def graphData(self, chartType, time_series: TimeSeries):
        #if 1 then bar graph
        if(chartType == 2):
            line_chart = pygal.Line(x_label_rotation=35)
            line_chart.title = f'Stock Data for {time_series.symbol}: {time_series.start_date} to {time_series.end_date}'
            time_series.series.reverse()
            line_chart.x_labels = [stock.date for stock in time_series.series]
            
            # use time_series.sersies for pygal chart
            open = [item.open for item in time_series.series]
            high = [item.high for item in time_series.series]
            low = [item.low for item in time_series.series]
            close = [item.close for item in time_series.series]
            line_chart.add('Open', open)
            line_chart.add('High', high)
            line_chart.add('Low', low)
            line_chart.add('Close', close)
            
            # show in browser with lxml
            line_chart.render_in_browser()
        if(chartType == 1):
            bar_chart = pygal.Bar(x_label_rotation=35)
            bar_chart.title = f'Stock Data for {time_series.symbol}: {time_series.start_date} to {time_series.end_date}'
            time_series.series.reverse()
            bar_chart.x_labels = [stock.date for stock in time_series.series]
            
            # use time_series.sersies for pygal chart
            open = [item.open for item in time_series.series]
            high = [item.high for item in time_series.series]
            low = [item.low for item in time_series.series]
            close = [item.close for item in time_series.series]
            bar_chart.add('Open', open)
            bar_chart.add('High', high)
            bar_chart.add('Low', low)
            bar_chart.add('Close', close)
            
            # show in browser with lxml
            bar_chart.render_in_browser()





