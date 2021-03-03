from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt 
import config
import pandas
import alpaca_profile


class AlphaVantageData:

    def __init__(self, symbol):
        self.sym = symbol
        self.ti = TechIndicators(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.ts = TimeSeries(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.ap = alpaca_profile.Profile()
        
    #def tradesma(self):
        #sma, ti_metadata = self.ti.get_sma(symbol=self.sym, interval='1min', time_period=60, series_type='close')
        #data_ts, metadata_ts = self.ts.get_intraday(symbol=self.sym,interval='1min', outputsize='full')

    def tradeBB(self):
        bb, bb_metadata = self.ti.get_bbands(symbol=self.sym, interval='60min', time_period=60)
        data_ts, metadata_ts = self.ts.get_intraday(symbol=self.sym, interval='60min', outputsize='full')
        #real vars taken from anthony
        real_middle = bb['2021-03-01 16:00:00']['Real Middle Band'].item()
        real_close = data_ts['2021-03-01 16:00:00']['4. close'].item()

        if(real_middle < real_close):  
            self.ap.send_basic_order( self.sym, 1, 'buy', 'bracket', 'gtc')
        
