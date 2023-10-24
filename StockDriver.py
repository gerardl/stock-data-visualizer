import os
from dotenv import load_dotenv
from StockService import StockService
import datetime

#get the Ticker Symbol
def getTik():
    print("Enter the stock symbol you are looking for: ")
    return input()
    
#get the chart type     
def getChartType():
    while True:
        print("Chart Types:")
        print("------------")
        print("1. Bar ")
        print("2. Line ")
        t = int(input())
        if t == 1 or t == 2:
            return t
        print("invalid option, try again. ")

#get the time series
def getTimeSeries():
    while True:
        print("Select the Time Series you want to generate:")
        print("--------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly")
        print("Enter the Time series option (1, 2, 3, 4)")
        ts = int(input())
        if ts == 1 or ts == 2 or ts ==3 or ts == 4:
            return ts
        print("invalid option, try again. ")

def getStartDate():
    print("Enter the Start Date (YYYY-MM-DD)")
    dStr = input()
    d = x = datetime.datetime(int(dStr[0:4]), int(dStr[5:7]), int(dStr[8:10]))
    return d

def getEndDate():
    print("Enter the End Date (YYYY-MM-DD)")
    dStr = input()
    d = x = datetime.datetime(int(dStr[0:4]), int(dStr[5:7]), int(dStr[8:10]))
    return d


def checkDates(sd, ed):
    if sd > ed:
        print("End Date must be after Start Date")
        return False
    else:
        return True


def goAgain():
    print("Would you like to view more stock Data?(y/n):")
    a = input()
    if a == "y":
        return True
    else:
        return False
    


def getStockData(service: StockService, ticker: str, time_series: int):
    if time_series == 1:
        return service.get_intraday(ticker)
    elif time_series == 2:
        return service.get_daily(ticker)
    elif time_series == 3:
        return service.get_weekly(ticker)
    elif time_series == 4:
        return service.get_monthly(ticker)


def main():
    load_dotenv()
    serv = StockService(os.getenv("API_KEY"))

    # Uncomment to test service without user input
    # temp_data = getStockData(serv, "AAPL", 2)
    # temp_filtered = temp_data.filter_date_range("2020-01-01", "2020-01-31")

    while True:
        ticker = getTik()
        chartType = getChartType()
        timeSeries = getTimeSeries()
        validDates = False
        while(validDates == False):
            startDate = getStartDate()
            endDate = getEndDate()
            validDates = checkDates(startDate, endDate)

        # get stock data from api
        stockData = getStockData(serv, ticker, timeSeries)
        # filter to specified date range
        # TODO: intra day filter is different than the others and needs some work
        filteredData = stockData.filter_date_range(startDate, endDate)

        if goAgain() == False:
            break

if __name__ == "__main__":     
    main()