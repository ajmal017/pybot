import requests
import json
from indicators_full import get_cci, get_ema, get_ppo, get_atr, get_sma
from kursdaten_wotd import get_stock_data_wotd
from time import sleep

stock_data = {}

def backtest(stock):

    #set indicators
    ema_co_long = 50
    ema_co_short = 25

    cci_length = 20

    ppo_length_short = 12
    ppo_length_long = 26

    atr_length = 14

    min_ppo_change = 0.2
    min_cci_change = 0

    #get stock data
    stock_data = get_stock_data_wotd(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        return

    #get indicator values
    cci = get_cci(stock_data, cci_length)

    ema_short = get_ema(stock_data, ema_co_short)
    ema_long = get_sma(stock_data, ema_co_long)

    ppo = get_ppo(stock_data, ppo_length_short, ppo_length_long)

    atr = get_atr(stock_data, atr_length)

    # Alle Listen so lange machen, wie die kürzeste, damit von hinten durchiteriert werden kann
    min_length = min(len(cci),len(ema_short),len(ema_long),len(ppo),len(atr))
    cci = cci[:min_length]
    ema_short = ema_short[:min_length]
    ppo = ppo[:min_length]
    atr = atr[:min_length]

    stock_data["open"] = stock_data["open"][:min_length]
    stock_data["high"] = stock_data["high"][:min_length]
    stock_data["low"] = stock_data["low"][:min_length]
    stock_data["close"] = stock_data["close"][:min_length]
    stock_data["volume"] = stock_data["volume"][:min_length]
    stock_data["date"] = stock_data["date"][:min_length]


    trade = {"position" : "$", "EK" : 0, "SL" : 0}
    sum = 10000
                                                        #ema_co_long größte Zahl
    for i in range(-1, (-1)*(len(stock_data["open"]) - ema_co_long),-1):

        cci_reversal = False

        if trade["position"] == "L":
            if (cci[i]<=-100) or ((cci[i] < 100) and ((ppo[i+1]-ppo[i]) >= min_ppo_change) and ((ppo[i+1]-ppo[i]) > (ppo[i+2]-ppo[i+1])) and ((cci[i+1]-cci[i]) >= min_cci_change)):
                print("CCI < -100 - Sold at " + str(stock_data["open"][i]) + " - Profit: " + str((stock_data["open"][i] - trade["EK"]) / trade["EK"]*100) + "%")
                sum += sum * ((stock_data["open"][i+1] - trade["EK"]) / trade["EK"])
                trade = {"position" : "$", "EK" : 0, "SL" : 0}

        elif trade["position"] == "S":
            if (cci[i]>=100) or ((cci[i]>=-100) and ((ppo[i]-ppo[i+1]) >= min_ppo_change) and ((ppo[i]-ppo[i+1]) > (ppo[i+1]-ppo[i+2])) and ((cci[i]-cci[i+1]) >= min_cci_change) and ((cci[i]-cci[i+1]) > 0)):
                print("CCI < -100 - Sold at " + str(stock_data["open"][i]) + " - Profit: " + str((trade["EK"]-stock_data["open"][i]) / trade["EK"]*100) + "%")
                sum +=  sum * ((trade["EK"]-stock_data["open"][i+1]) / trade["EK"])
                trade = {"position" : "$", "EK" : 0, "SL" : 0}

        #check trend with ema crossover
        if ema_short[i] > ema_long[i]:

            if trade["position"] == "S":
                print("EMA Cross against Trade - Sold at " + str(stock_data["open"][i]) + " - Profit: " + str((trade["EK"] - stock_data["open"][i]) / trade["EK"]*100) + "%")
                trade = {"position" : "$", "EK" : 0, "SL" : 0}
            #Kommt CCI aus Short-Trend und ist jetzt neutral/long?
            for k in range(1,3):
                if i+k > len(cci)-1:
                    cci_reversal = False

                elif (cci[i] > -100) and (cci[i+k] < -100):
                    cci_reversal = True
                    break

            #wenn CCI im Longtrend oder Reversal aus -100
            if (trade["position"] == "$") and ((cci[i] >= 100) or (cci_reversal)):

                #Wenn PPO und CCI steigen (mindestens um X) + PPO/CCI-Momentum -> PPO/CCI steigt stärker als am Vortag
                if ((ppo[i]-ppo[i+1]) >= min_ppo_change) and (ppo[i]-ppo[i+1] > ppo[i+1]-ppo[i+2]) and ((cci[i]-cci[i+1]) >= min_cci_change):

                    print("--------------------!!!--------------------")
                    print("GO LONG " + stock + " am " + str(stock_data["date"][i]) + " at " + str(stock_data["close"][i]))
                    print("Stop Loss 2D Low - 1 ATR: "+str(min(stock_data["low"][i], stock_data["low"][i+1], stock_data["low"][i+2])-atr[i]))
                    print("Stop Loss 2 ATR: "+str(stock_data["low"][i]-(2*atr[i])))
                    print("--------------------!!!--------------------")

                    trade["position"] = "L"
                    trade["EK"] = stock_data["close"][i]
                    trade["SL"] = min(stock_data["low"][i], stock_data["low"][i+1], stock_data["low"][i+2])-atr[i]

                elif ((ppo[i]-ppo[i+1]) >= min_ppo_change*0.7) and (ppo[i]-ppo[i+1] > ppo[i+1]-ppo[i+2]) and ((cci[i]-cci[i+1]) >= min_cci_change*0.7) and (cci[i]-cci[i+1] > cci[i+1]-cci[i+2]):
                    print("--------------------!!!--------------------")
                    print(stock+": about to show LONG signal")
                    print("--------------------!!!--------------------")



        elif ema_short[i] < ema_long[i]:

            if trade["position"] == "L":
                print("EMA Cross against Trade - Sold at " + str(stock_data["open"][i]) + " - Profit: " + str((stock_data["open"][i] - trade["EK"]) / trade["EK"]*100) + "%")
                trade = {"position" : "$", "EK" : 0, "SL" : 0}

            #Kommt CCI aus Long-Trend und ist jetzt neutral/short?
            for k in range(1,3):
                if (cci[i] < 100) and (cci[i+k] > 100):
                    cci_reversal = True
                    break

            #wenn CCI im Shorttrend oder Reversal aus 100
            if (trade["position"] == "$") and ((cci[i] <= -100) or (cci_reversal)):

                #Wenn PPO und CCI fallen (mindestens um X) + PPO-Momentum -> PPO fällt stärker als am Vortag
                if ((ppo[i+1]-ppo[i]) >= min_ppo_change) and (ppo[i+1]-ppo[i] > ppo[i+2]-ppo[i+1]) and ((cci[i+1]-cci[i]) >= min_cci_change):

                    print("--------------------!!!--------------------")
                    print("GO SHORT " + stock + " am " + str(stock_data["date"][i]) + " at " + str(stock_data["close"][i]))
                    print("Stop Loss 2D High - 1 ATR: "+str(max(stock_data["high"][i], stock_data["high"][i+1], stock_data["high"][i+2])+atr[i]))
                    print("Stop Loss 2 ATR: "+str(stock_data["high"][i]+(2*atr[i])))
                    print("--------------------!!!--------------------")

                    trade["position"] = "S"
                    trade["EK"] = stock_data["close"][i]
                    trade["SL"] = min(stock_data["high"][i], stock_data["high"][i+1], stock_data["high"][i+2])-atr[i]


                elif ((ppo[i+1]-ppo[i]) >= min_ppo_change*0.7) and (ppo[i+1]-ppo[i] > ppo[i+2]-ppo[i+1]) and ((cci[i+1]-cci[i]) >= min_cci_change*0.7) and (cci[i+1]-cci[i] > cci[i+2]-cci[i+1]):
                    print("--------------------!!!--------------------")
                    print(stock+": about to show SHORT signal")
                    print("--------------------!!!--------------------")

    print(sum)
