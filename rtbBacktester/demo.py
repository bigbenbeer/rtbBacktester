import rtbbacktester
import datetime

ticker = rtbbacktester.rtbTickers.Tickers.Forex.EURUSD()

ticker.startDate = datetime.datetime(year=2017, month=1, day=1)
ticker.endDate = datetime.datetime(year=2022, month=12, day=31)

print(ticker.symbol)
print(ticker.getDataframe())