import market_data as md
import trade_profile as tp
import config
import csv
import pandas as pd
import asyncio, datetime


market = md.MarketData('TSLA')
profile = tp.TradeProfile()


#print(market.get_security_price())
#market.show_barset()

''' Test Trader'''
#market.trade_macd()
market.trade_loop()
#market.setTicker('NVDA')

''' Test Orders '''
#profile.simple_order('NVDA', 10, 'buy', 'market', 'gtc')
#profile.close_position('NVDA')
#profile.bracket_buy('TSLA', 10, 'buy', 'market', 'gtc')