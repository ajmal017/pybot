import requests
import json
from indicators_full import get_hma, get_atr, get_sma, get_cci, get_wma
from kursdaten import get_stock_data_wotd
from time import sleep


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

    box = {"high" : 0, "low" : 0, "Trend" : 'UP', "Done" : True}

    box["high"] = stock_data[-1]["high"]
    box["low"] = stock_data[-1]["high"] - atr[-1]

    box_helper = 0
    cd_20 = 0
    box_count = 0

    highs_20 = []
    lows_20 = []

    print("Close: " + str(stock_data[0]))
    print("ATR1: " +  str(atr[0]))
    print("box high: " + str(box["high"]))
    print("box low: " + str(box["low"]))

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


        if (box["Done"] or box["Trend"] == "BUP") and stock_data[i]["high"] > box["high"] + atr[i]:

            if box["Trend"] == "DOWN" or box["Trend"] == "BUP":
                box_count = 0

            box["Done"] = False
            box["Trend"] = "UP"
            box["low"] = box["high"]
            box["high"] = stock_data[i]["high"]
            #print(stock_data[i]["date"] + ' ' + "new upbox " +str(box["high"]) + " " + str(box["low"]))

            cd_20 = 20

        if not box["Done"] and box["Trend"] == "UP":
            if stock_data[i]["high"] > box["high"]:
                box["high"] = stock_data[i]["high"]
                #print(stock_data[i]["date"] + " box high = " + str(box["high"]))
            elif stock_data[i]["high"] < box["high"] - 0.5*atr[i]:
                box["Trend"] = "BDOWN"
                #print(stock_data[i]["date"] + ' ' + "back down")

        if not box["Done"] and box["Trend"] == "BDOWN" and stock_data[i]["low"] > stock_data[i+1]["low"] + 0.5*atr[i]:
            box["low"] = stock_data[i+1]["low"]
            box["Done"] = True
            box["Trend"] = "UP"
            box_count += 1
            #print(stock_data[i]["date"] + ' ' + "upbox no. " + str(box_count) + " done")



##############WENN RUNTER##########################

        if (box["Done"] or box["Trend"] == "BDOWN") and stock_data[i]["low"] < box["low"] - atr[i]:

            if box["Trend"] == "UP" or  box["Trend"] == "BDOWN":
                box_count = 0

            box["Done"] = False
            box["Trend"] = "DOWN"
            box["high"] = box["low"]
            box["low"] = stock_data[i]["low"]
            #print(stock_data[i]["date"] + ' ' + "new downbox")

            cd_20 = 20

        if not box["Done"] and box["Trend"] == "DOWN":
            if stock_data[i]["low"] < box["low"]:
                box["low"] = stock_data[i]["low"]
            elif stock_data[i]["low"] > box["low"] + 0.5*atr[i]:
                box["Trend"] = "BUP"
                #print(stock_data[i]["date"] + ' ' + "back up")

        if not box["Done"] and box["Trend"] == "BUP" and stock_data[i]["high"] < stock_data[i+1]["high"] - 0.5*atr[i]:
            box["high"] = stock_data[i+1]["high"]
            box["Done"] = True
            box["Trend"] = "DOWN"
            box_count += 1
            #print(stock_data[i]["date"] + ' ' + "downbox no. " + str(box_count) + " done")

#########################################################################################

        if cd_20 < 0:

            if box["low"] < min(lows_20):
                box["low"] = min(lows_20)
            if box["high"] > max(highs_20):
                box["high"] = max(highs_20)


            lows_20 = lows_20[1:]
            highs_20 = highs_20[1:]

        lows_20.append(stock_data[i]["low"])
        highs_20.append(stock_data[i]["high"])
        cd_20 -= 1




        if trade["position"] == "$" and box["Done"] and box_count >= 3:

            if box["Trend"] == 'UP':

                trade["position"] = "L"
                trade["EK"] = stock_data[i]["close"]
                trade["Anzahl"] = round((0.005*sum)/(2.5*atr[i]))
                trade["SL"] = trade["EK"] - 2.5*atr[i]


                print("--------------------!!!--------------------")
                print("Buy " + str(trade["Anzahl"]) + " Stück für " + str(trade["EK"]) + " am " + str(stock_data[i]["date"]))
                print("Stop Loss: "+str(trade["SL"]))





###################################WENN LONG###########################################
        if trade["position"] == "L":

            l_count2 += 1

            '''
            if (stock_data[i]["low"] < trade["SL"]):

                print(str(stock_data[i]["date"]) + "Verkauf 1. Hälfte - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((trade["SL"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                print("sum = " + str(sum))
                trade["SL"] = 0
                trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}

            '''
            if (box["Trend"] == "DOWN" and box_count == 1 and not box["Done"]):

                print(str(stock_data[i]["date"]) + "Verkauf 2. Box - Profit: " + str((box["high"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((box["high"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (box["high"] - trade["EK"])*trade["Anzahl"] #box["high"] weil jetzt == altes box low
                print("sum = " + str(sum))
                trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}

            if (stock_data[i]["low"] < trade["SL"]):

                print(str(stock_data[i]["date"]) + "Verkauf SL - Profit: " + str((trade["SL"] - trade["EK"])*trade["Anzahl"]) +"€ "+ str((box["high"] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += (trade["SL"] - trade["EK"])*trade["Anzahl"]
                print("sum = " + str(sum))
                trade = {"position" : "$", "EK" : 0, "Anzahl" : 0, "SL" : 0, "TP": 0}


            #if trade["SL"] != 0:
                #trade["SL"] = box["low"] - atr[i]
                #print(stock_data[i]["date"] + ' ' + str(trade["SL"]<stock_data[i]["low"]))

    print(str(sum) + " " + str(l_count2) + "/" + str(l_count1))
