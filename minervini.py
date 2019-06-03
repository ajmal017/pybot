import requests
import json
from indicators_full import get_sma
from kursdaten_wotd import get_stock_data_wotd
from time import sleep

stock_data = {}

def check_trend(stock):

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        return

    #get indicator values
    sma_200 = get_sma(stock_data, 200)
    sma_150 = get_sma(stock_data, 150)
    sma_50 = get_sma(stock_data, 50)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    sma_150 = sma_150[:len(sma_200)]
    sma_50 = sma_50[:len(sma_200)]

    stock_data["open"] = stock_data["open"][:len(sma_200)]
    stock_data["high"] = stock_data["high"][:len(sma_200)]
    stock_data["low"] = stock_data["low"][:len(sma_200)]
    stock_data["close"] = stock_data["close"][:len(sma_200)]
    stock_data["volume"] = stock_data["volume"][:len(sma_200)]
    stock_data["date"] = stock_data["date"][:len(sma_200)]

    sma_200_steigt = True
    for i in range(min(30, len(sma_200)-1)):
        if (sma_200[i] < sma_200[i+1]):
            sma_200_steigt = False


    if (stock_data["close"][0] > sma_50[0]) and (sma_50[0] > sma_150[0]) and (sma_150[0] > sma_200[0]) and sma_200_steigt:

        print(stock + ' - Stage 2 Trend')

        avg_span = 0
        for i in range(30):
            avg_span += stock_data["high"][i]-stock_data["low"][i]
        avg_span = avg_span/30

        if (stock_data["high"][0]-stock_data["low"][0] < avg_span) and (stock_data["high"][1]-stock_data["low"][1] < avg_span):
            print('!!! niedrige Vola !!!')
