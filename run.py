import market_data
import csv
import pandas as pd
import asyncio, datetime
import config

md = market_data.MarketData('TSLA')

#md.show_barset('TSLA')
md.trade_loop()