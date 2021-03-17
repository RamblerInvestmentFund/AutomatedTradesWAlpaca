
#Pull technical data from AlphaVantage and place trades through Alpaca

#from alpha_vantage.techindicators import *
#import matplotlib.pyplot as plt 
#import pandas
import alpaca_profile as ap
import alpha_vantage_data as av
import ameritrade as am
import config
import time

#algo = av.AlphaVantageData('TSLA')
#profile = ap.Profile()
#algo.tradeBB()

america = am.Ameritrade('TSLA')
print(america.history["close"])
i=0
print(america.history["close"].size)
while(i<america.history["close"].size):
    print(america.history["close"][i])
    i=i+1
    time.sleep(1)
#america.get_history(key = america.key, symbol=america.sym, periodType='month', period=2, frequencyType='daily', frequency=1)
while(True):
    print("tesla price history:\n", america.history)
    time.sleep(5)