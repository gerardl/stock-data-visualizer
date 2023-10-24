import datetime
import os
from dotenv import load_dotenv

from StockService import StockService
from Models import Stock, TimeSeries
from StockExceptions import StockQueryException, StockQueryLimitException, StockEndpointException


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
    


def getStockData(service: StockService, ticker: str, time_series: int, start_date: datetime, end_date: datetime):
    try:
        if time_series == 1:
            return service.get_intraday(ticker, start_date, end_date)
        elif time_series == 2:
            return service.get_daily(ticker, start_date, end_date)
        elif time_series == 3:
            return service.get_weekly(ticker, start_date, end_date)
        elif time_series == 4:
            return service.get_monthly(ticker, start_date, end_date)
    except StockQueryLimitException as e:
        print("Sorry, but it looks like the supplied API key is over it's access limit. If you are using the intraday function, limit your date range to 5 months or less. Otherwise, please try again later.")
        return None
    except StockQueryException as e:
        print(f"Sorry, but there was an error with your query. Make sure you are using a valid stock symbol and try again. \nAdditional details:{e.message}")
        return None
    except StockEndpointException as e:
        print(f"Sorry, but there was an error with the API endpoint. Please try again later. \nAdditional details: {e.message}")
        return None
    except Exception as e:
        print(f"Sorry, but there was an unexpected error. Please try again later. \nAdditional details: {e.message}")
        return None


def main():
    load_dotenv()
    serv = StockService(os.getenv("API_KEY"))

    # Temp: Uncomment to test service without user input
    #temp_data = getStockData(serv, "AAPL", 2, datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31))
    #temp_intra = getStockData(serv, "AAPL", 1, datetime.datetime(2020, 1, 1), datetime.datetime(2020, 9, 28))
    #temp_week = getStockData(serv, "AAPL", 3, datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31))
    #temp_month = getStockData(serv, "AAPL", 4, datetime.datetime(2020, 1, 1), datetime.datetime(2020, 12, 31))

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
        # check if stock data was returned, otherwise an error occurred,
        # was printed, and we should continue to the next iteration or exit
        if stockData == None:
            continue
        
        if goAgain() == False:
            break

if __name__ == "__main__":     
    main()