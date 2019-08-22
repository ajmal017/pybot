import requests
import json
from indicators_full import get_atr, get_sma, get_cci
from kursdaten import get_stock_data_wotd
from time import sleep

def check_signal(stock):

    stock_data = {}
    output = []

    #get stock data
    sma_length = 50

    atr_1_length = 14
    cci_length = 20


    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        return

    #get indicator values
    sma = get_sma(stock_data, sma_length)

    atr_1 = get_atr(stock_data, atr_1_length)

    cci = get_cci(stock_data, cci_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(sma),len(atr_1), len(cci))

    sma = sma[:min_length]
    atr_1 = atr_1[:min_length]
    cci = cci[:min_length]

    stock_data = stock_data[:min_length]

    if ((stock_data[0]["close"] - stock_data[1]["close"]) >= 1.25*atr_1[1]) and ((sma[0] - sma[15]) > 0):
            l_high = 0
            for k in range(20):
                vol_avg += stock_data[k]["volume"]
                if stock_data[k]["high"] > l_high:
                    l_high = stock_data[k]["high"]

            vol_avg = vol_avg/20

            if (cci[0] * stock_data[0]["volume"]/vol_avg)  > 280 :
                    trade = {"EK" : 0, "Anzahl" : 0, "SL" : 0}
                    trade["EK"] = stock_data[0]["close"]
                    trade["SL"] = get_sl(stock)
                    trade["Anzahl"] = round(300/(trade["EK"] - trade["SL"]))

                    output.append(stock + " - " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + "SL = " + str(trade["SL"]))

    return output
