import pygal
import lxml
from Models import Stock, TimeSeries

class StockChart:
    def graphData(self, chartType, time_series: TimeSeries):
        #if 1 then bar graph
        if(chartType == 1):
            bar_chart = pygal.Bar()
            bar_chart.title = f'{time_series.symbol} Data'
            # use time_series.sersies for pygal chart
            for x in time_series.series:
                bar_chart.add(x.date, x.close)
            
            bar_chart.render_in_browser()