
#Pull technical data from AlphaVantage and place trades through Alpaca

#from alpha_vantage.techindicators import *
#import matplotlib.pyplot as plt 
#import pandas
import alpaca_profile as ap
import alpha_vantage_data as av
import config

algo = av.AlphaVantageData('TSLA')
profile = ap.Profile()
algo.tradeBB()