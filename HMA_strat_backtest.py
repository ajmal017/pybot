import requests
import json
from indicators_full import get_hma, get_atr, get_sma, get_cci
from kursdaten_wotd import get_stock_data_wotd
from time import sleep

stock_data = {}

def backtest(stock):

    #set indicators

    sma_length = 50

    cci_length = 100

    hma_1_length = 12
    hma_2_length = 25
    hma_3_length = 100

    atr_1_length = 14
    atr_2_length = 1



    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
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

    stock_data["open"] = stock_data["open"][:min_length]
    stock_data["high"] = stock_data["high"][:min_length]
    stock_data["low"] = stock_data["low"][:min_length]
    stock_data["close"] = stock_data["close"][:min_length]
    stock_data["volume"] = stock_data["volume"][:min_length]
    stock_data["date"] = stock_data["date"][:min_length]

    trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}
    sum = 50000

    l_count1 = 0
    l_count2 = 0
    last_high = 0

    for i in range(-1, (-1)*(len(stock_data["open"])),-1):

        l_count1 += 1

        """
        if (stock_data["date"][i] == "2016-03-01"):
            print("Close: " + str(stock_data["close"][i]))
            print("SMA50: " +  str(sma[i]))
            print("ATR1: " +  str(atr_1[i]))
            print("ATR2: " +  str(atr_2[i]))
            print("HMA50: " +  str(hma_1[i]))
            print("HMA75: " +  str(hma_2[i]))
            print("HMA100: " +  str(hma_3[i]))
            vol_avg = 0
            for k in range(20):
                vol_avg += stock_data["volume"][i]
            vol_avg = vol_avg/20
            print("Vol " +  str(stock_data["volume"][i]))
            print("Volavg " +  str(vol_avg))
        """

        if last_high < stock_data["high"][i]:
            last_high = stock_data["high"][i]

        if trade["position"] == "L":

            l_count2 += 1

            if (stock_data["low"][i] < trade["SL"]):
                print("SL hit - Sold at " + str(trade["SL"]) + " am " + str(stock_data["date"][i]))
                last_high = 0
                if (trade["TP"] > 0):
                    print("Verkauf - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
                    sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                    print("sum = " + str(sum))
                else:
                    print("Verkauf zweite Hälfte - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
                    sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                    print("sum = " + str(sum))
                trade = {"position" : "$", "EK" : 0, "SL" : 0, "TP": 0, "Anzahl" : 0}

            if (trade["SL"] < trade["EK"]) and (stock_data["high"][i] > trade["TP"]):
                '''
                print("Gewinnmitnahme (2.5 ATR) - Profit: " + str((trade["TP"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["TP"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (trade["TP"] - trade["EK"])*trade["Anzahl"]

                trade["TP"] = 0
                trade["Anzahl"] = trade["Anzahl"]/2
                '''
                trade["SL"] = trade["EK"]

            if (stock_data["low"][i] < trade["TP"]) and trade["SL"] > trade["EK"]: #SL > EK damit Gewinnmitnahme erst im Profit

                print("Gewinnmitnahme (2.5 ATR) - Profit: " + str((last_high - 3*atr_1[i] - trade["EK"])*trade["Anzahl"]/2) +"€ "+ str((last_high - 3*atr_1[i] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (last_high - 3*atr_1[i] - trade["EK"])*trade["Anzahl"]/2
                print("sum = " + str(sum))
                trade["TP"] = 0
                trade["Anzahl"] = trade["Anzahl"]/2


            if ((sma[i] - 1.5 * atr_1[i]) > trade["SL"]) and stock_data["high"][i] > (sma[i] - 1.5 * atr_1[i]):

                trade["SL"] = (sma[i] - 1.5 * atr_1[i])


        elif trade["position"] == "S":
            if (stock_data["high"][i] > trade["SL"]):
                print("SL hit - Sold at " + str(trade["SL"]) + " am " + str(stock_data["date"][i]) +" - Profit: " + str(trade["EK"]) - (trade["SL"] / trade["EK"]*100) + "%")
                sum +=  sum * ((trade["EK"] - trade["SL"]) / trade["EK"])
                trade = {"position" : "$", "EK" : 0, "SL" : 0, "TP": 0}

        if (cci[i] > 100) and (atr_2[i] > atr_1[i]):

            #if (hma_1[i] > hma_2[i]) and (hma_1[i] > hma_3[i]):

            if (((hma_1[i] - hma_1[i+1]) > 0) and ((hma_2[i] - hma_2[i+1]) > 0) and ((hma_3[i] - hma_3[i+1]) > 0) and ((sma[i] - sma[i+1]) > 0) and ((hma_1[i] - hma_1[i+1]) > (hma_1[i+1] - hma_1[i+2]))):

                vol_avg = 0

                for k in range(14):
                    vol_avg += stock_data["volume"][i+k]

                vol_avg = vol_avg/14

                if ((stock_data["volume"][i]*atr_2[i] > vol_avg*atr_1[i]) and (stock_data["close"][i] > stock_data["open"][i]) and (stock_data["close"][i] > stock_data["close"][i+1])):

                    if (trade["position"] != "L"):

                        trade["position"] = "L"
                        trade["EK"] = stock_data["close"][i]
                        trade["Anzahl"] = round((0.02*sum)/(2.5*atr_1[i]))
                        trade["SL"] = stock_data["close"][i] - (2.5*atr_1[i])
                        trade["TP"] = stock_data["close"][i] + (2.5*atr_1[i])


                        print("--------------------!!!--------------------")
                        print("Buy " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + " am " + str(stock_data["date"][i]))
                        print("Stop Loss 2.5 ATR: "+str(stock_data["close"][i]-(2.5*atr_1[i])))

                        break_even = trade["TP"]

                    if (trade["SL"] > break_even) and (stock_data["close"][i] > break_even):

                        l_anzahl = 0
                        l_anzahl = round((0.02*sum)/(stock_data["close"][i] - trade["SL"])) # 1% Risiko (Risiko = Abstand zum SL)

                        trade ["EK"] = ((trade["EK"] * trade["Anzahl"]) + (stock_data["close"][i] * l_anzahl)) / (trade["Anzahl"] + l_anzahl)
                        trade["Anzahl"] += l_anzahl
                        trade["TP"] = stock_data["close"][i] + (2.5*atr_1[i])

                        print("NACHKAUF " + str(l_anzahl) + " Stück für " + str(stock_data["close"][i]) + " am " + str(stock_data["date"][i]))
                        print("TP: " + str(trade["TP"]))

                        break_even = trade["TP"]






    print(str(sum) + " " + str(l_count2) + "/" + str(l_count1))
