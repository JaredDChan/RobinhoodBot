import config as cfg
import pandas as pd
import matplotlib.pyplot as plt
import sched
import time
from Robinhood import Robinhood
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from pprint import pprint

ts = TimeSeries(output_format='pandas')
data, metadata = ts.get_daily(symbol='MSFT', outputsize='full')
ti = TechIndicators(output_format='pandas')
pprint(data.head(2))

robinhood_client = Robinhood()
robinhood_client.login(username=cfg.USERNAME, password=cfg.PASSWORD,qr_code=cfg.QRCODE)

#getMarketPrice
stock_quote = robinhood_client.quote_data(listSymbol)
last_trade_price = stock_quote['last_trade_price']
print(last_trade_price)
# #Setup our variables, we haven't entered a trade yet and our RSI period
# enteredTrade = False
# rsiPeriod = 5
# #Initiate our scheduler so we can keep checking every minute for new price changes
# s = sched.scheduler(time.time, time.sleep)
# def run(sc): 
#     global enteredTrade
#     global rsiPeriod
#     print("Getting historical quotes")
#     # Get 5 minute bar data for Ford stock
#     historical_quotes = rh.get_historical_quotes("F", "5minute", "day")
#     closePrices = []

#  if (len(closePrices) > (rsiPeriod)):
#         #Calculate RSI
#         rsi = ti.rsi(DATA, period=rsiPeriod)
#         instrument = rh.instruments("F")[0]
#         #If rsi is less than or equal to 30 buy
#         if rsi[len(rsi) - 1] <= 30 and float(key['close_price']) <= currentSupport and not enteredTrade:
#             print("Buying RSI is below 30!")
#             rh.place_buy_order(instrument, 1)
#             enteredTrade = True
#         #Sell when RSI reaches 70
#         if rsi[len(rsi) - 1] >= 70 and float(key['close_price']) >= currentResistance and currentResistance > 0 and enteredTrade:
#             print("Selling RSI is above 70!")
#             rh.place_sell_order(instrument, 1)
#             enteredTrade = False
#         print(rsi)
#     #call this method again every 5 minutes for new price changes
#     s.enter(300, 1, run, (sc,))

# s.enter(1, 1, run, (s,))
# s.run()






# data['4. close'].plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()


# ti = TechIndicators(output_format='pandas')
# data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
# data.plot()
# plt.title('BBbands indicator for  MSFT stock (60 min)')
# plt.show()

# sp = SectorPerformances(output_format='pandas')
# data, meta_data = sp.get_sector()
# data['Rank A: Real-Time Performance'].plot(kind='bar')
# plt.title('Real Time Performance (%) per Sector')
# plt.tight_layout()
# plt.grid()
# plt.show()


# robinhood_client = Robinhood()
# robinhood_client.login(username=cfg.USERNAME, password=cfg.PASSWORD,qr_code=cfg.QRCODE)

# stock_instrument = robinhood_client.instruments('MSFT')[0]

# stock_quote = robinhood_client.quote_data("MSFT")

# print(robinhood_client.portfolios())

# print(stock_quote['last_trade_price'])

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()

# driver = webdriver.Chrome('chromedriver.exe')

# def LoginMethod(driver,config):
#     driver.get(config.WEBSITE_URL)
#     user_name = driver.find_element_by_name("username")
#     password = driver.find_element_by_name("password")

#     user_name.send_keys(config.USERNAME)
#     password.send_keys(config.PASSWORD)

#     driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/form/footer/div/button/span").click()
    
# LoginMethod(driver,config)

# driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div/footer/div[1]/button/span").click()