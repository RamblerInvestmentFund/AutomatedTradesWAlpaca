import requests
import yfinance as yf
import pandas as pd
import time, datetime
import numpy as np
import csv
import data_access as dao


def ema(f_name, period, signal=None):
    ''' 
    Calculate the Exponential Moving Average 
    EMA = (Current Close * (Smoothing/1+Days)) + Previous EMA * (1-(Smoothing/1+Days)))
        @params:
            period(int): The period over which the EMA is taken
        @return:
            Returns the full list of EMA values, incuding unused values as NaN
    '''

    # Read from file and create new df
    df = df = dao.read_data(f_name)
    df_size = len(df)-1

    # Set the initial EMA to the average of first n elements; obtain index of the position
    total = 0
    count = 0
    if (signal == None):
        for i in range(period):
            total += df.iloc[i]['Close']
            count+=1
    else:
        for i in range(26, period):
            total += df.iloc[i]['MACD']
            count+=1
    average = round(total/count, 4)
    ema_prev = average

    # Initialize elements before starting pos to NaN
    empty_list = np.empty(period-1)
    empty_list[:] = np.nan
    # from position period+1, calculate the EMA
    ema_list = [ema_prev]

    for i in range(period-1, df_size):
        close = df.iloc[i]['Close'] if (signal==None) else df.iloc[i]['MACD']
        factor = (2/(period+1))
        value = (close*factor) + (ema_prev*(1-factor))
        ema_prev = round(value, 4)
        ema_list.append(ema_prev)

    # Concatenate the emtpy list and list of values to create a new column
    full_list = [*empty_list, *ema_list]
    return full_list


def macd(f_name):
    ''' 
    Calculate the MACD 
    MACD = 12-Period EMA - 26-Period EMA
    Adds new columns to dataframe and writes to a new file
    '''

    df = dao.read_data(f_name)
    df_size = len(df)
    # Calculate the 12-day and 26-day ema
    ema_12 = ema(f_name=f_name, period=12)
    ema_26 = ema(f_name=f_name, period=26)

    # Calculate the macd
    macd = []
    for i in range(df_size):
        if(ema_12[i] != np.nan and ema_26[i] != np.nan):
            macd.append(ema_12[i] - ema_26[i])

    # Add new columns to the df
    df['EMA_12'] = ema_12
    df['EMA_26'] = ema_26
    df['MACD'] = macd
    # Write to file so that macd can be read
    df.to_csv(f_name, index=False)

    # Calculate the macd signal (9-day ema of macd)
    signal = ema(f_name=f_name, period=34, signal=1)
    df['MACD_Signal'] = signal

    # Calculate histogram (macd - signal)
    hist = []
    for i in range(df_size):
        if(macd[i] != np.nan and signal[i] != np.nan):
            hist.append(macd[i]-signal[i])
    df['Hist'] = hist
    
    # Write data to file
    df.to_csv(f_name, index=False)
 
