import requests
import json
from indicators_full import get_atr, get_sma, get_vcci
from kursdaten import get_stock_data_wotd
from time import sleep

stock_data = []

def backtest(stock):

    #set indicators

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

    trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}

    sum = 0
    avg = 0
    l_count = 0
    l_count2 = 0
    vol_avg = 0

    stops_15 = []
    for i in range(15):
        stops_15.append(0)

    for i in range(-1, (-1)*(len(stock_data)),-1):

        #Wurde STOP gerochen

        if (stock_data[i]["low"] < trade["SL"]):
            print("SL hit - Sold at " + str(trade["SL"]) + " am " + str(stock_data[i]["date"]))
            print("Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
            sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
            avg += l_count2*trade["Anzahl"]*trade["EK"]
            l_count2 = 0
            trade = {"position" : "$", "EK" : 0, "SL" : 0, "TP": 0, "Anzahl" : 0}

        #Neuer Stop ermitteln

        stops_15 = stops_15[1:]
        stops_15.append(stock_data[i]["high"]-5*atr_1[i])

        if trade["position"] == 'L':
            l_count += 1
            l_count2 += 1

            trade["SL"] = max(stops_15)

        #Check SIGNAL

        if (vcci > 200 and (stock_data[0]["close"] - stock_data[1]["close"]) >= atr_1[1]):
                l_high = 0
                vol_avg = 0

                for i in range(20):
                    vol_avg += stock_data[i]["volume"]

                vol_avg = vol_avg/20

                if stock_data[0]["volume"] > vol_avg:


                    for i in range(1, 100):
                        if l_high < stock_data[i]["close"]:
                            l_high = (stock_data[i]["close"]
                    if (stock_data[0]["close"] > l_high):

                        trade["EK"] = stock_data[i-1]["open"]
                        trade["SL"] = max(stops_15)

                        trade["Anzahl"] = round(300/(trade["EK"] - trade["SL"]))

                        trade["position"] = 'L'
                        print(stock + " BUY am " + stock_data[i]["date"] + ' Anzahl ' + str(trade["Anzahl"]) + ' Kurs ' +  str(trade["EK"]) +  " " + str(trade["EK"]*trade["Anzahl"]))





    avg = avg/l_count
    print(str(l_count) + ' Tage investiert')
    print("Durchschnittlich " + str(avg) + '€ investiert')
    print("Ergebnis " + str(sum/avg*100*220/l_count) + "% p.a. -> "+ str(sum) + "€")
