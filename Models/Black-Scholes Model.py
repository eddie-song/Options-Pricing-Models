import numpy as np
import yfinance as yf
import datetime
from datetime import datetime as dt
import math
from scipy.stats import norm

# select stock
stock = yf.Ticker("MSFT")

# get calls or puts
call_put = bool(int(input("Enter 0 for calls and 1 for puts: ")))

# retrieve an option
option_chain = stock.option_chain(stock.options[0])
if not call_put:
    options = option_chain.calls
else:
    options = option_chain.puts
option = options.iloc[50,:]

# retrieve option info
S = stock.info['currentPrice'] # underlying price
K = option["strike"] # strike price
r = 0.0551 # risk-free interest rate
v = option["impliedVolatility"] # volatility

# calculate time until maturity
date_format = '%Y-%m-%d' # format the date
expiration = dt.strptime(stock.options[1], date_format) # option expiration date
current = dt.today() # today's date
difference = expiration.date() - current.date() # days until expiration
T = difference.days / 365 # time to maturity

# calculate d1 and d2
# d1
d1 = (math.log(S/K) + (r + (v ** 2) * 0.5) * T) / (v * math.sqrt(T))
# d2
d2 = d1 - (v * math.sqrt(T))

# calculate the call or put option price
if not call_put:
    price = S * norm.cdf(d1) - (K * math.exp(-r * T)) * norm.cdf(d2)
else:
    price = K * math.exp(-r * T) * norm.cdf(-d2) - (S * norm.cdf(-d1))

# print theoretical option price
print(round(price,2))
