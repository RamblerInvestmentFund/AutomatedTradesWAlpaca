#Provides access to Alpaca papertrader account
import alpaca_trade_api as tradeapi
import config

class TradeProfile:
    def __init__(self):
        # API calls
        self.paca = tradeapi.REST(config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY,
                                  config.ALPACA_BASE_URL, api_version='v2')


    # Show Alpaca trading account balance
    def get_account_balance(self):
        account = self.paca.get_account()
        if account.trading_blocked:
            print('Account is currently restricted from trading.')
        print('${} is available as buying power.'.format(account.buying_power))
        return account


    # Get a list of info on current orders and positions
    def list_info(self):
        # List of orders
        my_orders = self.paca.list_orders()
        if not my_orders:
            print("No active orders")
        else:
            print(my_orders)

        # List of positions
        my_positions = self.paca.list_positions()
        if not my_positions:
            print("No current positions")
        else:
            print(my_positions)
    

    # Place an order
    # TODO: make this into a bracket order with stop/loss
    def place_order(self, symbol, qty, side, type, time_in_force):
        print('Placing order...')
        self.paca.submit_order(
            symbol=symbol,
            side=side,
            type=type,
            qty=qty,
            time_in_force=time_in_force)
        