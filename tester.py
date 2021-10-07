# import talib
import config as cfg
import pandas as pd
import matplotlib.pyplot as plt
import sched
import time
import logging
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from pprint import pprint
from datetime import datetime
import numpy as np
import alpaca_trade_api as tradeapi



api = tradeapi.REST(key_id = cfg.ALPACAID, secret_key = cfg.ALPACASECRET, base_url='https://paper-api.alpaca.markets')
account = api.get_account()
orders = api.list_orders()
currentPositions = api.list_positions()
assets = api.list_assets()

barTimeframe = "1Min" # 1Min, 5Min, 15Min, 1D
# ti = TechIndicators(output_format="json")
print(currentPositions)




iteratorPos = 0
assetsToTrade = ["SPY","TSLA"] #"ROKU","MRNA"
assetList = len(assetsToTrade)
listSymbol = assetsToTrade[iteratorPos]

low_SMA = "50"
high_SMA = "200"
alpha_SMAlow = api.alpha_vantage.techindicators(techindicator='SMA', symbol= listSymbol, interval='daily',time_period=low_SMA,series_type="close",output_format="json" )
alpha_SMAhigh = api.alpha_vantage.techindicators(techindicator='SMA', symbol= listSymbol, interval='daily',time_period=high_SMA,series_type="close",output_format="json" )
refresh_Date = [alpha_SMAlow['Meta Data']['3: Last Refreshed']]
str_Date = ' '.join([str(elem) for elem in refresh_Date]) 
SMAlow = alpha_SMAlow["Technical Analysis: SMA"][str_Date]["SMA"]
SMAhigh = alpha_SMAhigh["Technical Analysis: SMA"][str_Date]["SMA"]


# assetBARS = api.get_barset(assetsToTrade,barTimeframe,limit=10).df
# print(assetBARS)
# spyBARS['close'].plot()
# plt.show()

s = sched.scheduler(time.time, time.sleep)

def trade(sc):
    iteratorPos = 0
    assetsToTrade = ["SPY","TSLA"] #"ROKU","MRNA"
    assetList = len(assetsToTrade)
    listSymbol = assetsToTrade[iteratorPos]

    if currentPositions in assetsToTrade:
        openPosition = api.get_position(listSymbol)
    else:
        openPosition = 0
        positionSizing = 0.25
        cashBalance = float(api.get_account().cash)
        print(cashBalance)
        lastPrice = api.get_barset(listSymbol,barTimeframe,limit=1).df
        askPrice =  lastPrice.iloc[0,3]
        askPrice.item()
        print(askPrice)
    
        targetPositionSize = cashBalance / (askPrice / positionSizing) # Calculates required position size
        print(account.status)
        
        while iteratorPos < assetList:
            print("SMA" + low_SMA + ": " + SMAlow)
            print("SMA" + high_SMA + ": " + SMAhigh)
            # Calculates the trading signals
            if SMAlow > SMAhigh:
                print("SMA" + low_SMA + " is greater than " + high_SMA)
                # Opens new position if one does not exist
                if openPosition == 0:
                    
                    
                    
                    returned = api.submit_order(symbol=listSymbol,qty=int(targetPositionSize),side="buy",type="market",time_in_force="day") # Market order to open position
                    print(returned)
                    print("opened new position")
                    
            else:
                if openPosition == 0:
                    print('nothing changed')
                # Closes position if SMA20 is below SMA50
                else:
                    openPosition = api.get_position(listSymbol)
                
                    returned = api.submit_order(symbol=listSymbol,qty=int(targetPositionSize),side="sell",type="market",time_in_force="day") # Market order to fully close position
                    print(returned)
                    print("closed position")

            iteratorPos += 1
        s.enter(10, 1, trade, (sc,))

s.enter(1, 1, trade, (s,))
s.run()


# # Tracks position in list of symbols to download
# iteratorPos = 0 
# assetListLen = len(assetsToTrade)

# while iteratorPos < assetListLen:
# 	symbol = assetsToTrade[iteratorPos]
	
# 	returned_data = api.get_bars(symbol,barTimeframe,limit=100).bars
	
# 	timeList = []
# 	openList = []
# 	highList = []
# 	lowList = []
# 	closeList = []
# 	volumeList = []

# 	# Reads, formats and stores the new bars
# 	for bar in returned_data:
# 		timeList.append(datetime.strptime(bar.time,'%Y-%m-%dT%H:%M:%SZ'))
# 		openList.append(bar.open)
# 		highList.append(bar.high)
# 		lowList.append(bar.low)
# 		closeList.append(bar.close)
# 		volumeList.append(bar.volume)
	
# 	# Processes all data into numpy arrays for use by talib
# 	timeList = np.array(timeList)
# 	openList = np.array(openList,dtype=np.float64)
# 	highList = np.array(highList,dtype=np.float64)
# 	lowList = np.array(lowList,dtype=np.float64)
# 	closeList = np.array(closeList,dtype=np.float64)
# 	volumeList = np.array(volumeList,dtype=np.float64)

# 	# Calculated trading indicators
#   spyRSI = api.alpha_vantage.techindicators(techindicator='RSI',output_format='JSON',symbol="SPY",interval='60min',time_period='200',series_type='close')
# 	SMA20 = talib.SMA(closeList,20)[-1]
# 	SMA50 = talib.SMA(closeList,50)[-1]
# 	iteratorPos += 1


