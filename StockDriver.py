import datetime
import os
from dotenv import load_dotenv

from StockService import StockService
from StockChart import StockChart
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

        try: 
            ts = int(input())
            if ts in [1, 2, 3, 4]:  
                return ts 
            else:
                print("Invalid option, try again.")
        except ValueError: 
            print("Invalid input, please enter a number between 1 and 4.")
selected_time_series = getTimeSeries()
print(f"You selected option {selected_time_series}")


def getStartDate():
    try:
        print("Enter the Start Date (YYYY-MM-DD)")
        dStr = input()
        d = x = datetime.datetime(int(dStr[0:4]), int(dStr[5:7]), int(dStr[8:10]))
        return d
    except ValueError:
        print("Invalid Date. Try again.")
        return getStartDate()

def getEndDate():
    try:
        print("Enter the End Date (YYYY-MM-DD)")
        dStr = input()
        d = x = datetime.datetime(int(dStr[0:4]), int(dStr[5:7]), int(dStr[8:10]))
        return d
    except ValueError:
        print("Invalid Date. Try again.")
        return getEndDate()


def checkDates(sd, ed, ts):
    # ensure that intraday is only 30 days max
    if ts == 1:
        if sd < ed:
            if sd + datetime.timedelta(days=30) < ed:
                print("Due to insufficient API access, Intraday data can only be generated for a maximum of 30 days.")
                return False
            else:
                return True
        else:
            print("End Date must be after Start Date")
            return False
    # ensure that the start date is before the end date
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
    try:
        load_dotenv()
        serv = StockService(os.getenv("API_KEY"))
        chart_serv = StockChart()
        
        while True:
            ticker = getTik()
            chartType = getChartType()
            timeSeries = getTimeSeries()
            validDates = False
            while(validDates == False):
                startDate = getStartDate()
                endDate = getEndDate()
                validDates = checkDates(startDate, endDate, timeSeries)

            # get stock data from api
            stockData = getStockData(serv, ticker, timeSeries, startDate, endDate)
            # check if stock data was returned, otherwise an error occurred,
            # was printed, and we should continue to the next iteration or exit
            if stockData == None or stockData.series == None or len(stockData.series) == 0:
                continue
            # graph the data
            chart_serv.graphData(chartType, stockData)
            
            if goAgain() == False:
                break
    except Exception as e:
        print(f"Sorry, but there was an unexpected error. Please try again later. \nAdditional details: {e.message}")
        exit()

if __name__ == "__main__":     
    main()