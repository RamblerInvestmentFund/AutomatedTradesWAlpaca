
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
#america.get_history(key = america.key, symbol=america.sym, periodType='month', period=2, frequencyType='daily', frequency=1)
while(True):
    print("tesla price history:\n", america.history)
    time.sleep(5)