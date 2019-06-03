import requests
import json
from indicators_full import get_cci, get_ema, get_ppo, get_atr, get_sma
from kursdaten_wotd import get_stock_data_wotd
from time import sleep

stock_data = {}

def backtest(stock):

    #set indicators
    sma_long_len = 100
    ema_short_len = 38

    cci_length = 20

    atr_length = 14

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        return

    #get indicator values
    cci = get_cci(stock_data, cci_length)

    ema_short = get_ema(stock_data, ema_short_len)
    sma_long = get_sma(stock_data, sma_long_len)

    atr = get_atr(stock_data, atr_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(cci),len(ema_short),len(sma_long),len(atr))
    cci = cci[:min_length]
    ema_short = ema_short[:min_length]
    atr = atr[:min_length]

    stock_data["open"] = stock_data["open"][:min_length]
    stock_data["high"] = stock_data["high"][:min_length]
    stock_data["low"] = stock_data["low"][:min_length]
    stock_data["close"] = stock_data["close"][:min_length]
    stock_data["volume"] = stock_data["volume"][:min_length]
    stock_data["date"] = stock_data["date"][:min_length]

    trade = {"position" : "$", "EK" : 0, "SL" : 0}
    sum = 10000
    cci_reversal = False
                                                        #sma_long_len größte Zahl
    for i in range(-1, (-1)*(len(stock_data["open"])),-1):

        if (trade["position"] == "$"):
            cci_reversal = False
        elif (trade["position"] == "L") and (cci[i] > 0):
            cci_reversal = False
        elif (trade["position"] == "S") and (cci[i] < 0):
            cci_reversal = False

        if trade["position"] == "L":
            if ((cci[i]<0) and (cci[i+1]<0) and (cci[i] < cci[i+1]) and not cci_reversal) or (cci[i] < -100):
                print("CCI = " + str(cci[i]) + " - Sold at " + str(stock_data["open"][i-1]) + " am " + str(stock_data["date"][i]) +" - Profit: " + str((stock_data["open"][i-1] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += sum * ((stock_data["open"][i-1] - trade["EK"]) / trade["EK"])
                trade = {"position" : "$", "EK" : 0, "SL" : 0}
                cci_reversal = False

        elif trade["position"] == "S":
            if ((cci[i]>0) and (cci[i+1]>0) and not cci_reversal) or (cci[i] > 100):
                print("CCI = " + str(cci[i]) + " - Sold at " + str(stock_data["open"][i-1]) + " - Profit: " + str((trade["EK"]-stock_data["open"][i-1]) / trade["EK"]*100) + "%")
                sum +=  sum * ((trade["EK"] - stock_data["open"][i-1]) / trade["EK"])
                trade = {"position" : "$", "EK" : 0, "SL" : 0}
                cci_reversal = False

        #check trend with ema crossover
        if ema_short[i] > sma_long[i]:

            if trade["position"] == "S":
                print("EMA Cross against Trade - Sold at " + str(stock_data["open"][i-1]) + " - Profit: " + str((stock_data["open"][i-1] - trade["EK"]) / trade["EK"]*100) + "%")
                trade = {"position" : "$", "EK" : 0, "SL" : 0}

            #Kommt CCI aus Short-Trend und ist jetzt neutral/long?
            for k in range(1,3):
                if i+k > len(cci)-1:
                    cci_reversal = False

                elif (cci[i] > -100) and (cci[i+k] < -100):
                    cci_reversal = True
                    break

            '''
            print("LONG")
            print("DATE " + str(stock_data["date"][i]))
            print("POS " + trade["position"])
            print("CCI " + str(cci[i]))
            print("CCI Rev " + str(cci_reversal))
            print("EMA heute " + str(ema_short[i]))
            print("EMA gestern " + str(ema_short[i+1]))
            print("SMA heute " + str(sma_long[i]))
            '''

            ema_momentum = ((ema_short[i] - ema_short[i+1]) > 0) and ((ema_short[i] - ema_short[i+1]) > (ema_short[i+1] - ema_short[i+2])) and ((ema_short[i+1] - ema_short[i+2]) > (ema_short[i+2] - ema_short[i+3]))
            sma_momentum = ((sma_long[i] - sma_long[i+1]) > 0.0015) and ((sma_long[i] - sma_long[i+1]) > (sma_long[i+1] - sma_long[i+2])) and ((sma_long[i+1] - sma_long[i+2]) > (sma_long[i+2] - sma_long[i+3]))

            rel_abstand_ema_sma = ((ema_short[i] - sma_long[i])/sma_long[i] > 0.05) and ((ema_short[i] - sma_long[i]) > (ema_short[i+1] - sma_long[i+1]))

            #wenn CCI im Longtrend oder Reversal aus -100 und ema steigt
            if (trade["position"] == "$") and ((cci[i] > 0) or (cci_reversal)) and (cci[i] > cci[i+1]) and (ema_momentum) and (sma_momentum) and (rel_abstand_ema_sma):

                    print("--------------------!!!--------------------")
                    print("GO LONG am " + str(stock_data["date"][i]) +" at "+ str(stock_data["close"][i]))
                    print("Stop Loss 2D Low - 1 ATR: "+str(min(stock_data["low"][i], stock_data["low"][i+1], stock_data["low"][i+2])-atr[i]))
                    print("Stop Loss 2 ATR: "+str(stock_data["low"][i]-(2*atr[i])))
                    print("--------------------!!!--------------------")

                    trade["position"] = "L"
                    trade["EK"] = stock_data["close"][i]
                    trade["SL"] = min(stock_data["low"][i], stock_data["low"][i+1], stock_data["low"][i+2])-atr[i]


'''
        elif ema_short[i] < sma_long[i]:

            if trade["position"] == "L":
                print("EMA Cross against Trade  - Sold at " + str(stock_data["open"][i-1]) + " - Profit: " + str((trade["EK"]-stock_data["open"][i-1]) / trade["EK"]*100) + "%")
                trade = {"position" : "$", "EK" : 0, "SL" : 0}

            #Kommt CCI aus Long-Trend und ist jetzt neutral/short?
            for k in range(1,3):
                if (cci[i] < 100) and (cci[i+k] > 100):
                    cci_reversal = True
                    break


            print("SHORT")
            print("DATE " + str(stock_data["date"][i]))
            print("POS " + trade["position"])
            print("CCI " + str(cci[i]))
            print("CCI Rev " + str(cci_reversal))
            print("EMA heute " + str(ema_short[i]))
            print("EMA gestern " + str(ema_short[i+1]))
            print("SMA heute " + str(sma_long[i]))


            ema_momentum = ((ema_short[i] - ema_short[i+1]) < 0) and ((ema_short[i] - ema_short[i+1]) < (ema_short[i+1] - ema_short[i+2])) and ((ema_short[i+1] - ema_short[i+2]) < (ema_short[i+2] - ema_short[i+3]))

            #wenn CCI im Shorttrend oder Reversal aus 100
            if (trade["position"] == "$") and ((cci[i] < 0) or (cci_reversal)) and (ema_momentum):

                    print("--------------------!!!--------------------")
                    print("GO SHORT am " + str(stock_data["date"][i]) +" at "+str(stock_data["close"][i]))
                    print("Stop Loss 2D High - 1 ATR: "+str(max(stock_data["high"][i], stock_data["high"][i+1], stock_data["high"][i+2])+atr[i]))
                    print("Stop Loss 2 ATR: "+str(stock_data["high"][i]+(2*atr[i])))
                    print("--------------------!!!--------------------")

                    trade["position"] = "S"
                    trade["EK"] = stock_data["close"][i]
                    trade["SL"] = min(stock_data["high"][i], stock_data["high"][i+1], stock_data["high"][i+2])-atr[i]



            print(cci[i])
            print(sma_long[i])
            print(ema_short[i])
            print(stock_data["open"][i])
            print(stock_data["close"][i])
            print(stock_data["high"][i])
            print(stock_data["low"][i])
            print(stock_data["date"][i])


    print(sum)'''
