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
        endpoint = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory?apikey={key}&periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}"
        #data_request = self.get_data(key, symbol, periodType, period, frequencyType, frequency)
        #print("status code: ",data_request.status_code)
        
        p = pandas.json_normalize(self.get_data_from_endpoint(endpoint), record_path=['candles'])
        #print("data: ",data)
        #print("data: ",p)
        return p

    def get_data_from_endpoint(self, endpoint):
        
        data_request = requests.get(endpoint, params={'apikey': self.key})
        data = json.loads(data_request.content)
        return data

    def tradeBB(self):
        history = self.history

        for item in (history):
            item['30 Day MA'] = item["close"].rolling(window=20).mean()
    
            # set .std(ddof=0) for population std instead of sample
            item['30 Day STD'] = item["close"].rolling(window=20).std() 
            
            item['Upper Band'] = item["close"] + (item['30 Day STD'] * 2)
            item['Lower Band'] = item["close"] - (item['30 Day STD'] * 2)

