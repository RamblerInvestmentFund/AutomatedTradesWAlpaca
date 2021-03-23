import csv
import yfinance as yf
import pandas as pd
import time


TEST_CSV = 'closing_data_daily.csv'

''' Write the closes of a stock for 1 month period/hourly frequency '''
def write_data(ticker, f_name):
    # Create closing price history df
    stock = yf.Ticker(ticker)
    data = stock.history(period='1mo', interval='1h')
    hist = pd.DataFrame(data=data, columns=['Close'])
    hist.reset_index(inplace=True)

    #hist = trader.get_hist('1mo', '1h')
    hist_size = len(hist)
    mk_time_list = []

    # Create new column for mk time
    for i in range(hist_size):
        local_time = str((hist.iloc[i]['Date']))
        date_mk = time.mktime(time.strptime(local_time, '%Y-%m-%d %H:%M:%S'))
        mk_time_list.append(date_mk)

    # Write mk date and close price to file
    date_col = hist['Date']
    hist = hist.drop(['Date'], axis=1)
    hist.insert(loc=0, column='MK_Time', value=mk_time_list)
    #hist.insert(loc=2, column='Date', value=date_col)
    hist.to_csv(f_name, index=False)


''' Read csv into data frame'''
def read_data(f_name):
    df = pd.read_csv(f_name)
    return df


def get_data_size(f_name):
    df = pd.read_csv(f_name)
    return len(df)-1

write_data('SPY', TEST_CSV)
''' Test Data 
write_data('SPY', TEST_CSV)
print(read_data(TEST_CSV))
'''