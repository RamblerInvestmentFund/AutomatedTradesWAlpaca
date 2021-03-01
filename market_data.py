from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import matplotlib.pyplot as plt
import asyncio, datetime
import csv
import config 
import trade_profile


# Market data from Alphavantage
class MarketData:
    def __init__(self, ticker):
        # Class vars
        self.ticker = ticker
        # API calls
        self.tind = TechIndicators(key=config.ALPHA_VANTAGE_KEY, output_format='pandas') # Note: tech indicators does't support csv
        self.ts = TimeSeries(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.tp = trade_profile.TradeProfile()
        # Tech indicators list
        self.big_mac, meta = self.tind.get_macd(symbol=self.ticker, interval='1min')


    # Set the stock ticker 
    def setTicker(self, ticker):
        self.ticker = ticker


    # Get the current price of a security
    def get_security_price(self):
        data, meta = self.ts.get_quote_endpoint(self.ticker)
        df = pd.DataFrame(data=data)
        current_price = float(df.iloc[0][4])
        return current_price
        
        
    # Get daily historic data for a specified period and write to a csv
    def show_barset(self):
        historic_data, meta = self.ts.get_daily_adjusted(self.ticker, outputsize='compact')
        historic_data.plot()
        plt.title('Historic prices for {}'.format(self.ticker))
        plt.show()
        

    # Logic to trade macd
    # Places a buy order if MACD is 2% above signal line, closes position if 2% below signal
    def trade_macd(self):
        self.big_mac, meta = self.tind.get_macd(symbol=self.ticker, interval='1min', series_type='close')
        df = pd.DataFrame(self.big_mac, columns=['MACD','MACD_Signal'])
        # Get MACD and MACD Signal
        macd = float(df.iloc[0]['MACD'])
        signal = float(df.iloc[0]['MACD_Signal'])

        print(df)
        print('macd is: {}'.format(macd))
        print('signal is: {}'.format(signal))

        if (macd > signal*1.02 and macd > 0):
            print('Trading on MACD')
            self.tp.simple_order(self.ticker, qty=10, side='buy', type='market', time_in_force='gtc')
        elif (macd < signal*0.98 and macd <= 0):
            print('MACD is 2% below the signal, closing exisiting positions')
            self.tp.close_position(self.ticker)
        else:
            print('No trades made')

    
    # Initialize the trade loop: checks indicators on minute
    def trade_loop(self): 
        # instantiate event loop
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self.update_indicators())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()


    # check indicators every minute
    async def update_indicators(self):
        while True:
            print('checking indicators...')
            self.trade_macd()
            print(self.big_mac)
            await asyncio.sleep(60)

    
   
