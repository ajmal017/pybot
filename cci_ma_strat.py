import requests
import json
from indicators_full import get_sma
from kursdaten_wotd import get_stock_data_wotd
from time import sleep

stock_data = {}

def check_signal(stock):

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        return

    #get indicator values
    sma_100 = get_sma(stock_data, 100)
    ema_38 = get_ema(stock_data, 38)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    ema_38 = ema_38[:len(sma_100)]


    stock_data["open"] = stock_data["open"][:len(sma_100)]
    stock_data["high"] = stock_data["high"][:len(sma_100)]
    stock_data["low"] = stock_data["low"][:len(sma_100)]
    stock_data["close"] = stock_data["close"][:len(sma_100)]
    stock_data["volume"] = stock_data["volume"][:len(sma_100)]
    stock_data["date"] = stock_data["date"][:len(sma_100)]

    #Kommt CCI aus Short-Trend und ist jetzt neutral/long?
    if (stock_data["close"][0] > ema_38[0]) and (ema_38[0] > sma_100[0]):

        for i in range(3):
            if (cci[i] > -100) and (cci[i+1] < -100):
            cci_reversal = True
            break

        ema_momentum = ((ema_38[0] - ema_38[1]) > 0) and ((ema_38[0] - ema_38[1]) > (ema_38[1] - ema_38[2])) and ((ema_38[1] - ema_38[2]) > (ema_38[2] - ema_38[3]))
        sma_momentum = ((sma_100[0] - sma_100[1]) > 0.0015) and ((sma_100[0] - sma_100[1]) > (sma_100[1] - sma_100[2])) and ((sma_100[1] - sma_100[2]) > (sma_100[2] - sma_100[3]))

        rel_abstand_ema_sma = ((ema_38[0] - sma_100[0])/sma_100[0] > 0.05) and ((ema_38[0] - sma_100[0]) > (ema_38[1] - sma_100[1]))

        #wenn CCI im Longtrend oder Reversal aus -100 und ema steigt
        if ((cci[0] > 0) or (cci_reversal)) and (cci[0] > cci[1]) and (ema_momentum) and (sma_momentum) and (rel_abstand_ema_sma):

            print(stock + ' - Kaufsignal')
