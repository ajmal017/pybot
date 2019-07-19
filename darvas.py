import requests
import json
from indicators_full import get_hma, get_atr, get_sma, get_cci, get_wma
from kursdaten import get_stock_data_wotd
from time import sleep
import Queue


stock_data = []

def backtest(stock):

    #set indicators
    atr_length = 14




    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        return

    atr = get_atr(stock_data, atr_length)
    atr = atr[:len(atr)]
    stock_data = stock_data[:len(atr)]


    trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}
    sum = 50000

    l_count1 = 0
    l_count2 = 0

    box = {"high" : 0, "low" : 0, "Trend" : 'UP', "Done" : False}

    box["high"] = stock_data[i]["high"]
    box["low"] = stock_data[i]["high"] - atr[i]
    box_helper = 0

    print("Close: " + str(stock_data[0]))
    print("ATR1: " +  str(atr[0]))
    print("box high: " + box_high)
    print("box low: " + box_low)

    for i in range(-1, (-1)*(len(stock_data)),-1):
        '''
        if stock_data[i]["date"] == '2015-09-17':

                print("Close: " + str(stock_data[i]))
                print("SMA50: " +  str(sma[i]))
                print("ATR1: " +  str(atr[i]))
                print("ATR2: " +  str(atr_2[i]))
                print("HMA1: " +  str(hma_1[i]))
                print("HMA2: " +  str(hma_2[i]))
                print("HMA3: " +  str(hma_3[i]))
                print("CCI: " +  str(cci[i]))
                vol_avg = 0
                for k in range(14):
                    vol_avg += stock_data[i+k]["volume"]
                vol_avg = vol_avg/14
                print("Vol " +  str(stock_data[i]["volume"]))
                print("Volavg " +  str(vol_avg))
        '''


        l_count1 += 1



##################WENN AUFWÄRTS################


        if box["Done"] and stock_data[i]["high"] > box["high"] + atr[i]:
            box["Done"] = False
            box["Trend"] = "UP"
            box["low"] = box["high"]
            box["high"] = stock_data[i]["high"]

            cd_20 = 20
            q = Queue.Queue()

        if not box["Done"] and stock_data[i]["high"] > box["high"]:
            box["high"] = stock_data[i]["high"]

        if not box["Done"] and box["Trend"] = "UP" and stock_data[i]["high"] < box["high"]:
            box["Trend"] = "DOWN"

        if not box["Done"] and stock_data[i]["low"] > box["low"]:
            box_helper = stock_data[i]["low"]

        if not box["Done"] and box["Trend"] = "DOWN" and stock_data[i]["low"] > box_helper:
            box["low"] = box_helper
            box["Done"] = True

        if cd_20 < 0:
            box["low"] = min(list)
            list = list[1:]

        list.append(stock_data[i]["low"])
        cd_20 -= 1














###################################WENN LONG###########################################
        if trade["position"] == "L":

            l_count2 += 1

            if (trade["TP"] != 0) and (trade["TP"] < last_high - 3*atr[i]):
                trade["TP"] = last_high - 3*atr[i]

            if (stock_data[i]["low"] < trade["SL"]):
                print("SL hit - Sold at " + str(trade["SL"]) + " am " + str(stock_data[i]["date"]))
                last_high = 0
                last_low = 0
                if (trade["TP"] > 0):
                    print("Verkauf - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
                    sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                    print("sum = " + str(sum))
                else:
                    print("Verkauf zweite Hälfte - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
                    sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                    print("sum = " + str(sum))
                trade = {"position" : "$", "EK" : 0, "SL" : 0, "TP": 0, "Anzahl" : 0}

            if (trade["SL"] < trade["EK"]) and (stock_data[i]["high"] > trade["TP"]):
                '''
                print("Gewinnmitnahme (2.5 ATR) - Profit: " + str((trade["TP"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["TP"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (trade["TP"] - trade["EK"])*trade["Anzahl"]

                trade["TP"] = 0
                trade["Anzahl"] = trade["Anzahl"]/2
                '''
                trade["SL"] = trade["EK"]

            if (trade["TP"] > 0) and (stock_data[i]["low"] < trade["TP"]) and trade["SL"] > trade["EK"]: #SL > EK damit Gewinnmitnahme erst im Profit

                print("Gewinnmitnahme (2.5 ATR) - Profit: " + str((trade["TP"] - trade["EK"])*trade["Anzahl"]/2) +"€ "+ str((trade["TP"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (trade["TP"] - trade["EK"])*trade["Anzahl"]/2
                print("sum = " + str(sum))
                trade["TP"] = 0
                trade["Anzahl"] = trade["Anzahl"]/2


            if ((sma[i] - 1.5 * atr[i]) > trade["SL"]) and stock_data[i]["high"] > (sma[i] - 1.5 * atr[i]):

                trade["SL"] = (sma[i] - 1.5 * atr[i])


#####################################GO LONG##################################################
        if (cci[i] > 100) and (atr_2[i] > atr[i]):

            #if (hma_1[i] > hma_2[i]) and (hma_1[i] > hma_3[i]):

            if (((hma_1[i] - hma_1[i+1]) > 0) and ((hma_2[i] - hma_2[i+1]) > 0) and ((hma_3[i] - hma_3[i+1]) > 0) and ((sma[i] - sma[i+1]) > 0) and ((hma_1[i] - hma_1[i+1]) > (hma_1[i+1] - hma_1[i+2]))):

                vol_avg = 0

                for k in range(14):
                    vol_avg += stock_data[i+k]["volume"]

                vol_avg = vol_avg/14

                if ((stock_data[i]["volume"]*atr_2[i] > vol_avg*atr[i]) and (stock_data[i]["close"] > stock_data[i]["open"]) and (stock_data[i]["close"] > stock_data[i+1]["close"])):

                    if (trade["position"] != "L"):

                        trade["position"] = "L"
                        trade["EK"] = stock_data[i]["close"]
                        trade["Anzahl"] = round((0.02*sum)/(2.5*atr[i]))
                        trade["SL"] = stock_data[i]["close"] - (2.5*atr[i])
                        trade["TP"] = stock_data[i]["close"] + (2.5*atr[i])


                        print("--------------------!!!--------------------")
                        print("Buy " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + " am " + str(stock_data[i]["date"]))
                        print("Stop Loss 2.5 ATR: "+str(trade["SL"]))

                        break_even = trade["TP"]

                    if (trade["SL"] > break_even) and (stock_data[i]["close"] > break_even):

                        l_anzahl = 0
                        l_anzahl = round((0.02*sum)/(stock_data[i]["close"] - trade["SL"])) # 1% Risiko (Risiko = Abstand zum SL)

                        trade ["EK"] = ((trade["EK"] * trade["Anzahl"]) + (stock_data[i]["close"] * l_anzahl)) / (trade["Anzahl"] + l_anzahl)
                        trade["Anzahl"] += l_anzahl
                        trade["TP"] = stock_data[i]["close"] + (2.5*atr[i])

                        print("NACHKAUF " + str(l_anzahl) + " Stück für " + str(stock_data[i]["close"]) + " am " + str(stock_data[i]["date"]))
                        print("TP: " + str(trade["TP"]))

                        break_even = trade["TP"]



    print(str(sum) + " " + str(l_count2) + "/" + str(l_count1))
