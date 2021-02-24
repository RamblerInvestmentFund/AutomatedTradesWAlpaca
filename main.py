
#Pull technical data from AlphaVantage and place trades through Alpaca

from alpha_vantage.techindicators import *
import matplotlib.pyplot as plt 
import pandas

ti = TechIndicators(key='6IRQ2UGMYR33M3DC', output_format='pandas')
data , metadata = ti.get_sma(symbol='TSLA', interval='60min', time_period=20)
data.plot()
plt.title('simple moving average time series for tesla stock (60 min)')
plt.show()