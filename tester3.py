# import talib
import config as cfg
import pandas as pd
import matplotlib.pyplot as plt
import sched
import time
import logging
from Robinhood import Robinhood
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from pprint import pprint
from datetime import datetime
import numpy as np
import alpaca_trade_api as tradeapi

#Configuration
api = tradeapi.REST(key_id = cfg.ALPACAID, secret_key = cfg.ALPACASECRET, base_url='https://paper-api.alpaca.markets')
account = api.get_account()
orders = api.list_orders()
currentPositions = api.list_positions()
assets = api.list_assets()
print(account.status)

s = sched.scheduler(time.time, time.sleep)


#Assets
assetsToCheck = ["TSLA","SPY"] #"ROKU","MRNA"

#getBalances
positionSizing = .25
cashBalance = float(api.get_account().cash)
print("Current Account Balance: ")
print(cashBalance)

#Buy Thresholds
upward_Trend_Threshold = 1.50
dip_Threshold = -.25

#Sell Thresholds
PROFIT THRESHOLDd = .25
stop_Loss_Threshold = -2.00


barTimeframe = "15Min" # 1Min, 5Min, 15Min, 1D
#getPreviousPrice
def getPreviousPrice(stock):
    prevPrice = api.get_barset(listSymbol,barTimeframe,limit=2).df
    previousPrice = prevPrice.iloc[0,3]
    previousPrice.item()
    print(listSymbol + " Price " + barTimeframe + " ago: ")
    print(previousPrice)
    return previousPrice
    

#getMarketPrice
def getMarketPrice(stock):
    lastPrice = api.get_barset(listSymbol,barTimeframe,limit=1).df
    latestPrice = lastPrice.iloc[0,3]
    latestPrice.item()
    print(listSymbol + " Latest Price: ")
    print(latestPrice)
    return latestPrice


#placeBuyOrder
def placeBuyOrder(listSymbol):
    buyOrderPrice = getMarketPrice(listSymbol)
    targetPositionSize = cashBalance / (buyOrderPrice / positionSizing) # Calculates required position size
    print("Projected Quantity to Buy: ")
    print(targetPositionSize)
    returned = api.submit_order(symbol=listSymbol,qty=int(targetPositionSize),side="buy",type="market",time_in_force="day")
    print(returned)

#placeSellOrder
def placeSellOrder(listSymbol):
    sellOrderPrice = getMarketPrice(listSymbol)
    targetPositionSize = cashBalance / (sellOrderPrice / positionSizing) # Calculates required position size
    print("Projected Quantity to Sell: ")
    print(targetPositionSize)
    returned = api.submit_order(symbol=listSymbol,qty=int(targetPositionSize),side="sell",type="market",time_in_force="day")
    print(returned)

#check prices before you make decision to buy or sell

def buyOrSell():
    
    for listSymbol in assetsToCheck:      
        comparePrice = getPreviousPrice(listSymbol)
        currentPrice = getMarketPrice(listSymbol)
        percentageDiff = (currentPrice - comparePrice)/comparePrice*100
        if percentageDiff >= upward_Trend_Threshold or percentageDiff <= dip_Threshold:
            print(percentageDiff)
            isNextOperationBuy = False
        elif percentageDiff >= profit_Threshold or percentageDiff <= stop_Loss_Threshold:
            print(percentageDiff)
            isNextOperationBuy = True
        else:
            print("Price has not changed enough to buy or sell")
    return isNextOperationBuy
#how do i know when to stop buying or selling


def attemptTrade(pp):
    # for listSymbol in assetsToCheck:      
    #     comparePrice = getPreviousPrice(listSymbol)
    #     currentPrice = getMarketPrice(listSymbol)
    
    #     percentageDiff = (currentPrice - comparePrice)/comparePrice*100
        
        if pp:
            placeBuyOrder(listSymbol)
            print("Placed Buy Order!")
                

        elif pp:            
            placeSellOrder(listSymbol)
            print("Placed Sell Order!")

        else:
            print('Another Error Happened')
        
    
# def runBot(sc,isNextOperationBuy):
    

#     s.enter(30, 1, runBot, (sc,buyOrSell(),attemptTrade(buyOrSell()))))


# s.enter(1, 1, runBot, (s,isNextOperationBuy))
# s.run()

print(buyOrSell())