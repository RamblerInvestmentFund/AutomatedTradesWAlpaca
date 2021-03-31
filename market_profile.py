import alpaca_trade_api as tradeapi
import yfinance as yf
import config
import pandas as pd

# MarketProfile provides basic access to Alpaca trading account
class MarketProfile:
    def __init__(self):
        # API calls
        self.paca = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY,
                                  config.ALPACA_BASE_URL, api_version='v2')


    # Check if a position is held
    def has_position(self, symbol):
        try:
            position = self.paca.get_position(symbol)
            return True
        except:
            return False


    # Close exisiting position on a stock
    def close_position(self, symbol):
        try:
            position = self.paca.get_position(symbol)
            print('Closing position for {}...\n'.format(symbol))
            self.paca.close_position(symbol)
        except:
            print('No positions held for {}\n'.format(symbol))


    # Place a simple order
    def simple_order(self, symbol, qty, side, type, time_in_force):
        # Get quote endpoint
        current_price = self.get_price(symbol)
        print(current_price)
        print('Placing order...')
        # Place an order
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=type,
            qty=qty,
            time_in_force=time_in_force,
        )
        print('Bought 10 shares of {}\n'.format(symbol))


    # Place a bracket order
    def bracket_order(self, symbol, qty, side, type, time_in_force):
        # Get quote endpoint
        current_price = self.get_price(symbol)
        print('Placing order for {}'.format(symbol))
        # Place an order with stop loss @ -10%; take profit @ +2%
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=type,
            qty=qty,
            time_in_force=time_in_force,
            order_class='bracket',
            stop_loss={'stop_price': current_price * 0.90,
                         'limit price': current_price * 0.91},
            take_profit={'limit_price': current_price * 1.02}
        )
        print('Bought 10 shares of {} at {} per share with stop price @ -5% and limit @ +3%\n'.format(symbol, current_price))


    # Get the current asking price using yfinance
    def get_price(self, ticker):
        stock =  yf.Ticker(ticker)
        current = stock.info.get('ask')
        return current
        
    
mp = MarketProfile()
#print(mp.get_price('SPY'))