from alpha_vantage.techindicators import *
import matplotlib.pyplot as plt 
import config
import pandas
import profile


class AlphaVantageData:

    def __init__(self, symbol):
        self.sym = symbol
        self.ti = TechIndicators(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.profile = profile.Profile()
        self.sma = self.ti.get_sma(symbol=self.sym, interval='60min', time_period=20)
        