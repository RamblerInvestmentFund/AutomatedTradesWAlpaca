# AutomatedTradesWAlpaca
# Collin's branch
- Pull stock data from AlphaVantage to place trades with various technical strategies

# todo
- automate better by make sure the script does not just repeat the same thing evey 2 minutes. Make sure it knows it put down a order last time it ran.
- try another strat other than macd and bbands

# automation
- This will be done with cron
- Cron is a daemon that runs scripts in the background of your computer. it does not take up a lot of resources to run as it's meant to run scripts for admins
- the format would look like this ...

```
* * * * * command(s)
^ ^ ^ ^ ^
| | | | |     allowed values
| | | | |     -------
| | | | ----- Day of week (0 - 7) (Sunday=0 or 7)
| | | ------- Month (1 - 12)
| | --------- Day of month (1 - 31)
| ----------- Hour (0 - 23)
------------- Minute (0 - 59)
```

- for our trading algos, it could look something like this ...

```
 */2 9-17 * * 1-5 cd /home/quant/trade_algo/ && /usr/bin/python3 /home/quant/trade_algo/main.py >> /var/log/quant.log 2>&1
```

- this job will run 9am-5pm on weekdays. It will run every 2 minutes

# Trading Strat
- macd, buy when 4% above singal line, sell when 4% below signal line
- bbands, if price moves to upper band then get ready to sell, if prices moves to lower band then get ready to buy.
- combine macd and bbands (have not started this yet)
