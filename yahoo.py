import requests
import yfinance as yf
import pandas as pd
import time, datetime
import numpy as np
import csv
import hist_dw as hdw

class Yahoo:
    def __init__(self, ticker):
        self.stock =  yf.Ticker(ticker)

    
    def avg(self, start_pos, end_pos=None):
        ''' 
        Compute the average over a given interval 
            @params:
                start_pos(int): number of days from the current time to begin computing the average
                end_pos(int): Optional ending position for average timeframe. Defaults to averaging 
                              from starting pos to the oldest entry (start of the list)
        '''
        
        df = hdw.read_data('closing_data_daily.csv')
        # Get the starting and ending positions in seconds
        current_time = time.time()
        start = current_time - (start_pos*86400)
        # If no end position is specified, set the end to the oldest row mk time ("first" entry in df)
        end = current_time - (end_pos*86400) if (end_pos!=None) else df.iloc[0]['MK_Time']
        df_size = len(df)-1
        total = 0
        count = 0
        # Search for starting pos from the most recent entry (bottom of the file)
        for i in range(df_size, 0, -1):
            mk_time = df.iloc[i]['MK_Time']
            # if mk time is between start and end, get total and count. If the time is greater than the start, move on. Else, we have passed the end
            if (mk_time <= start and mk_time >= end):
                total += df.iloc[i]['Close']
                count+=1
            elif (mk_time > start):
                continue
            else:
                break
        average = round(total/count, 4)
        return average
    

    def starting_avg(self, period):
        ''' 
        Caluclate starting average needed for EMA 
            @params: 
                period(int): The number of days over which to average, beginning with the oldest entry in the df
            @return:
                Returns a tuple of the average and starting index
        '''

        df = hdw.read_data('closing_data_daily.csv')
        df_size = len(df)-1
        data_range = df.iloc[0]['MK_Time'] + (period*86400)
        total = 0
        count = 0
        for i in range(0, df_size):
            mk_time = df.iloc[i]['MK_Time']
            if (mk_time <= data_range):
                total += df.iloc[i]['Close']
                count+=1
            else:
                break
        starting_idx = count-1
        average = round(total/count, 4)
        return average, starting_idx
        

    def ema(self, period):
        ''' 
        Calculate the Exponential Moving Average 
        EMA = (Current Value * (Smoothing/1+Days)) + Previous EMA * (1-(Smoothing/1+Days)))
            @params:
                period(int): The period over which the EMA is taken
                col_name(str): The name of the new df column
            @return:
                Returns the full list of EMA values, incuding unused values as NaN
        '''

        # Read from file and create new df
        df = hdw.read_data('closing_data_daily.csv')
        df_size = len(df)-1
        # Set the initial EMA to the average of first n elements; obtain index of the position
        ema_prev = self.starting_avg(period)[0]
        start_pos = self.starting_avg(period)[1]+1
        # Initialize elements before starting pos to NaN
        empty_list = np.empty(start_pos)
        empty_list[:] = np.nan

        # from position period+1, calculate the EMA
        ema_list = [ema_prev]
        for i in range(start_pos, df_size):
            close = df.iloc[i]['Close']
            factor = (2/(period+1))
            value = (close*factor) + (ema_prev*(1-factor))
            ema_prev = round(value, 4)
            ema_list.append(ema_prev)

        # Concatenate the emtpy list and list of values to create a new df column
        full_list = [*empty_list, *ema_list]
        return full_list


    def macd(self):
        ''' 
        Calculate the MACD 
        MACD = 12-Period EMA - 26-Period EMA
        Adds new columns to dataframe and writes to a new file
        '''

        # Calculate the 12-day and 26-day ema
        ema_12 = self.ema(12)
        ema_26 = self.ema(26)

        # Calculate the macd
        macd = []
        for i in range(len(ema_12)):
            if(ema_12[i] != np.nan and ema_26[i] != np.nan):
                macd.append(ema_12[i] - ema_26[i])
        #print('\nmacd is: {}'.format(macd))

        # Add new columns to the df and write to a new file
        df = hdw.read_data('closing_data_daily.csv')
        df['EMA_12'] = ema_12
        df['EMA_26'] = ema_26
        df['MACD'] = macd
        df.to_csv('macd_output.csv', index=False)
        

trader = Yahoo('SPY')
#print(trader.ema(12))
trader.macd()
#print(trader.starting_avg(12))

#print(trader.get_price())
#print(trader.sma(5))



