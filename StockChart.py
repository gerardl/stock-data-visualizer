import pygal
from datetime import datetime, timedelta
import lxml
import Utility as util
from Models import Stock, TimeSeries

class StockChart:
    def graphData(self, chartType, time_series: TimeSeries):
        #if 1 then bar graph
        if(chartType == 1):
            bar_chart = pygal.Bar()
            bar_chart.title = f'Stock Data for {time_series.symbol}: {time_series.start_date} to {time_series.end_date}'
            date_range = [time_series.start_date + timedelta(days=i) for i in range((time_series.end_date - time_series.start_date).days + 1)]
            date_strings = [date.strftime('%Y-%m-%d') for date in date_range]

            # use time_series.sersies for pygal chart
            #bar_chart.x_labels = map(str, range(time_series.start_date, time_series.end_date))
            bar_chart.x_labels = date_strings
            open = [item['open'] for item in time_series.series]
            high = [item['high'] for item in time_series.series]
            low = [item['low'] for item in time_series.series]
            close = [item['close'] for item in time_series.series]
            bar_chart.add('Open', open)
            bar_chart.add('High', high)
            bar_chart.add('Low', low)
            bar_chart.add('Close', close)
            # for x in time_series.series:
                
            #     bar_chart.add(x.date, [x.open, x.high, x.low, x.close])
            # bar_chart.x_labels = map(str, range(time_series.start_date, time_series.end_date))
            
            bar_chart.render_in_browser()





