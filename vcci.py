import requests
import json
from indicators_full import get_atr, get_sma, get_vcci
from kursdaten import get_stock_data_wotd
from time import sleep

def check_signal(stock):

    stock_data = {}
    output = []

    #get stock data
    sma_length = 50

    atr_1_length = 14
    vcci_length = 20


    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        return

    #get indicator values
    sma = get_sma(stock_data, sma_length)

    atr_1 = get_atr(stock_data, atr_1_length)

    vcci = get_vcci(stock_data, vcci_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(sma),len(atr_1), len(vcci))

    sma = sma[:min_length]
    atr_1 = atr_1[:min_length]
    vcci = vcci[:min_length]

    stock_data = stock_data[:min_length]

    output.append(str(vcci[0]))
    if (vcci[0] > 200 and (stock_data[0]["close"] - stock_data[1]["close"]) >= atr_1[1]):
        l_high = 0
        vol_avg = 0

        for i in range(20):
            vol_avg += stock_data[i]["volume"]

        vol_avg = vol_avg/20

        if stock_data[0]["volume"] > vol_avg:


            for i in range(1, 100):
                if l_high < stock_data[i]["close"]:
                    l_high = stock_data[i]["close"]

            if (stock_data[0]["close"] > l_high):

                stops_15 = []
                for i in range(15):
                    stops_15.append(stock_data[i]["high"]-5*atr_1[i])

                trade = {"EK" : 0, "Anzahl" : 0, "SL" : 0}
                trade["EK"] = stock_data[0]["close"]
                trade["SL"] = max(stops_15)
                trade["Anzahl"] = round(300/(trade["EK"] - trade["SL"]))

                output.append(stock + " - " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + "SL = " + str(trade["SL"]))

    return output
