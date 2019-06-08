import requests
import json
from indicators import get_sma, get_hma, get_atr, get_cci
from kursdaten_wotd import get_stock_data_wotd
from time import sleep



def check_signal(stock):

    stock_data = {}
    output = []
    sum = 50000

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        return


    sma_length = 50

    cci_length = 100

    hma_1_length = 12
    hma_2_length = 25
    hma_3_length = 100

    atr_1_length = 14
    atr_2_length = 1



    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        return

    #get indicator values


    sma = get_sma(stock_data, sma_length)

    atr_1 = get_atr(stock_data, atr_1_length)
    atr_2 = get_atr(stock_data, atr_2_length)

    hma_1 = get_hma(stock_data, hma_1_length)
    hma_2 = get_hma(stock_data, hma_2_length)
    hma_3 = get_hma(stock_data, hma_3_length)

    cci = get_cci(stock_data, cci_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(hma_3),len(hma_2),len(hma_1),len(sma),len(atr_1),len(atr_2), len(cci))
    sma = sma[:min_length]
    atr_1 = atr_1[:min_length]
    atr_2 = atr_2[:min_length]
    hma_1 = hma_1[:min_length]
    hma_2 = hma_2[:min_length]
    hma_3 = hma_3[:min_length]
    cci = cci[:min_length]

    stock_data = stock_data[:min_length]


    print(sma[0])
    print(atr_1[0])
    print(atr_2[0])
    print(hma_1[0])
    print(hma_2[0])
    print(hma_3[0])
    print(cci[0])



    if ((cci[0] > 100) and ((hma_1[0] - hma_1[1]) > 0) and ((hma_2[0] - hma_2[1]) > 0) and ((hma_3[0] - hma_3[1]) > 0) and ((sma[0] - sma[1]) > 0) and ((hma_1[0] - hma_1[1]) > (hma_1[1] - hma_1[2]))):

                output.append("--------------------" + stock + "--------------------")

                vol_avg = 0

                for i in range(14):
                    vol_avg += stock_data[i]["volume"]

                vol_avg = vol_avg/14

                if ((stock_data[0]["volume"]*atr_2[0] > vol_avg*atr_1[0]) and (stock_data[0]["close"] > stock_data[0]["open"]) and (stock_data[0]["close"] > stock_data[1]["close"])):

                    trade = {"EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}
                    trade["EK"] = stock_data[0]["close"]
                    trade["Anzahl"] = round((0.02*sum)/(2.5*atr_1[0]))
                    trade["SL"] = stock_data[0]["close"] - (2.5*atr_1[0])
                    trade["TP"] = stock_data[0]["close"] + (2.5*atr_1[0])

                    output.append("Buy " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]))
                    output.append("ATR = " + str(atr_1[0]))
                    output.append("Stop Loss 2.5 ATR: "+str(trade["SL"]))
                    output.append("Take Profit 2.5 ATR: "+str(trade["TP"]))

    if len(output) == 0:
        output.append(stock + ' - No Signal')

    return output
