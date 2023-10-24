from StockService import StockService

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
    return input()

def getEndDate():
    print("Enter the End Date (YYYY-MM-DD)")
    return input()

def goAgain():
    print("Would you like to view more stock Data?(y/n):")
    a = input()
    if a == "y":
        return True
    else:
        return False

def main():
    
    #temp
    ticker = "MSFT"
    serv = StockService("demo")
    result = serv.get_daily_data(ticker)
    print(result)

    while True:
        ticker = getTik()
        chartType = getChartType()
        timeSeries = getTimeSeries()
        startDate = getStartDate()
        endDate = getEndDate()
        if goAgain() == False:
            break
        



main()