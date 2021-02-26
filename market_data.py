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
        # Class variables
        self.ticker = ticker
        # API calls
        self.tind = TechIndicators(key=config.ALPHA_VANTAGE_KEY, output_format='pandas') # Note: tech indicators does't support csv
        self.ts = TimeSeries(key=config.ALPHA_VANTAGE_KEY, output_format='pandas')
        self.tp = trade_profile.TradeProfile()
        # Tech indicators list
        self.big_mac, meta = self.tind.get_macd(symbol=self.ticker, interval='1min')


    # Get daily historic data for a specified period and write to a csv
    def show_barset(self):
        historic_data, meta = self.ts.get_daily_adjusted(ticker, outputsize='compact')
        historic_data.plot()
        plt.title('Historic prices for {}'.format(self.ticker))
        plt.show()
        

    # Logic to trade macd
    # Trade macd if current signal is greater than earlier signal
    # (NOTE: this is just to test api connections and async update, 
    # NOT a good trade strategy!!!)
    def trade_macd(self):
        self.big_mac, meta = self.tind.get_macd(symbol=self.ticker, interval='1min', series_type='close')
        df = pd.DataFrame(self.big_mac, columns=['MACD','MACD_Signal'])
        # place order if signal has increased (again, probably not a good strategy irl)
        if (df.iloc[0]['MACD_Signal'] > df.iloc[1]['MACD_Signal']):
            print('Trading on macd')
            self.tp.place_order(self.ticker, qty=10, side='buy', type='market', time_in_force='gtc')
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