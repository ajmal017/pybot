import requests
import json
from indicators_full import get_atr, get_sma, get_rsi
from kursdaten import get_stock_data_wotd
from time import sleep

def check_signal(stock):

    stock_data = {}
    output = []

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        output.append(stock + ' ZERO VALUES!')
        return output

    #set indicators

    sma_length = 50

    atr_1_length = 14

    rsi_length = 14

    #get indicator values
    sma = get_sma(stock_data, sma_length)
    atr_1 = get_atr(stock_data, atr_1_length)
    rsi = get_rsi(stock_data, rsi_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(sma),len(atr_1), len(rsi))

    sma = sma[:min_length]
    atr_1 = atr_1[:min_length]
    rsi = rsi[:min_length]

    stock_data = stock_data[:min_length]

    if ((stock_data[0]["close"] - stock_data[1]["close"]) >= 1.5*atr_1[1]) and rsi[0] > 50:
        if  ((sma[0] - sma[1]) > 0) and ((sma[0] - sma[15]) > 0):

            vol_avg = 0
            for k in range(14):
                vol_avg += stock_data[k]["volume"]

            vol_avg = vol_avg/14

            if (rsi[0] < 75 and stock_data[0]["volume"] > 2*vol_avg) or stock_data[0]["volume"] > 3.5*vol_avg:

                    stops_15 = []
                    for i in range(15):
                        stops_15.append(stock_data[i]["high"]-5*atr[i])
                        
                    trade = {"EK" : 0, "Anzahl" : 0, "SL" : 0}
                    trade["EK"] = stock_data[0]["close"]
                    trade["SL"] = max(stops_15)
                    trade["Anzahl"] = round(300/(trade["EK"] - trade["SL"]))

                    output.append(stock + " - " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + "SL = " + str(trade["SL"]))

    return output
