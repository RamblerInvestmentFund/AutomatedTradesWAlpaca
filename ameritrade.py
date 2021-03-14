import requests
import config
import json
import pandas
import alpaca_profile

class Ameritrade:
    def __init__(self, symbol):
        self.sym = symbol
        self.key = config.AMERITRADE_KEY
        self.ap = alpaca_profile.Profile()
        self.history = self.get_history(key = self.key, symbol=self.sym, periodType='month', period=2, frequencyType='daily', frequency=1)

    def get_history(self, key, symbol, periodType, period, frequencyType, frequency):
        #https://api.tdameritrade.com/v1/marketdata/TSLA/pricehistory?apikey=0U0QZB1EEZNVKFRQEKKAQHLKEH0BOGSR&periodType=month&period=2&frequencyType=daily&frequency=1 
        endpoint = "https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory?apikey={key}&periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}".format(symbol=symbol, key=key, periodType=periodType, period=period, frequencyType=frequencyType, frequency=frequency)
        data_request = requests.get(endpoint, params={'apikey': key})
        #print("status code: ",data_request.status_code)
        data = json.loads(data_request.content)
        p = pandas.json_normalize(data, record_path=['candles'])
        #print("data: ",data)
        #print("data: ",p)
        return p

    #def tradeBB(self):

