import requests
import json
import pandas as pd
import config
import time
        

# Get the latest price of a stock
def get_current_price(ticker):
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes?'.format(ticker)
    page = requests.get(url=endpoint, params={'apikey': config.AMERITRADE_KEY})
    content = json.loads(page.content)
    df = pd.DataFrame(data=content)
    return float(df.loc['regularMarketLastPrice'])


# Get the price history
def get_history(ticker, periodType, period, frequencyType, frequency): 
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{ticker}/pricehistory?periodType={periodType}' \
        '&period={period}&frequencyType={frequencyType}&frequency={frequency}'.format(
            ticker=ticker, periodType=periodType, period=period, frequencyType=frequencyType, frequency=frequency)

    #short_endpoint = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(ticker)
    
    page = requests.get(url=endpoint, params={'apikey': config.AMERITRADE_KEY})
    content = json.loads(page.content)
    #print(content)
    df = pd.json_normalize(content, record_path=['candles'])
    return df
    #return content


# Caluclate the Simple Moving Average
# ***num is the day range over which SMA is calculated***
def sma(ticker, num):
    # Get current Epoch time in ms
    current_time = round(time.time()*1000)
    # Get the range of days; converted to ms
    num_range = current_time - (num*86400000)
    # Get the Historical DataFrame
    df = get_history(ticker=ticker, periodType='month', period=2, frequencyType='daily', frequency=1)
    # Set the iterator to the total number of rows, 
    i=len(df)-1
    total =0 
    count =0
    # While the date time is greater than the date range, retrieve the sum and count
    while (df.iloc[i]['datetime'] >= num_range):
        total += df.iloc[i]['close']
        count=count+1 
        i=i-1
    val = total/count
    return val


# Calculate the Exponential Moving Average 
def ema(ticker, num):
    # Get the average of the last n days
    # This will be the previous ema
    ema_prev = sma(ticker, num)
    print('sma is: {}'.format(ema_prev))
    # Get the current price; this will be a stand-in for closing price
    # TODO: Switch this to previous mkt close
    current = get_current_price(ticker)
    print('current price is: {}'.format(current))
    print(current)
    # Get the smoothing factor
    factor = (2/(num+1))
    val = (current * factor) + (ema_prev*(1-factor))
    return round(val, 4)


''' TEST BLOCK '''
#get_history(ticker='SPY', periodType='month', period=1, frequencyType='daily', frequency=1)
#print(get_history(ticker='SPY', periodType='month', period=2, frequencyType='daily', frequency=1))
#sma('SPY', 5)
print(ema('SPY', 5))