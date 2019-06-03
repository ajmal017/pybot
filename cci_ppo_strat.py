import requests
import json
from indicators import get_cci, get_ema, get_ppo, get_atr, get_sma
from kursdaten import get_stock_data
from time import sleep


def check_signal(stock):

    sleep(3)

    #set indicators
    ema_co_long = 50
    ema_co_short = 25

    cci_length = 20

    ppo_length_short = 12
    ppo_length_long = 26

    atr_length = 14

    min_ppo_change = 0.2
    min_cci_change = 20

    #get stock data
    stock_data = get_stock_data(stock)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        return

    #get indicator values
    cci = get_cci(stock_data, cci_length)

    ema_short = get_ema(stock_data, ema_co_short)
    ema_long = get_sma(stock_data, ema_co_long)

    ppo = get_ppo(stock_data, ppo_length_short, ppo_length_long)

    atr = get_atr(stock_data, atr_length)

    cci_reversal = False


    #check trend with ema crossover
    if ema_short[0] > ema_long[0]:

        #Kommt CCI aus Short-Trend und ist jetzt neutral/long?
        for i in range(1,3):
            if (cci[0] > -100) and (cci[i] < -100):
                cci_reversal = True
                print("CCI Reversal")
                break

        #wenn CCI im Longtrend oder Reversal aus -100
        if (cci[0] >= 100) or (cci_reversal):

            #Wenn PPO und CCI steigen (mindestens um X) + PPO/CCI-Momentum -> PPO/CCI steigt stärker als am Vortag
            if ((ppo[0]-ppo[1]) >= min_ppo_change) and (ppo[0]-ppo[1] > ppo[1]-ppo[2]) and ((cci[0]-cci[1]) >= min_cci_change) and (cci[0]-cci[1] > cci[1]-cci[2]):

                print("--------------------!!!--------------------")
                print("GO LONG "+stock+" at "+str(stock_data["close"][0]))
                print("Stop Loss 2D Low - 1 ATR: "+str(min(stock_data["low"][0], stock_data["low"][1], stock_data["low"][2])-atr[0]))
                print("Stop Loss 2 ATR: "+str(stock_data["low"][0]-(2*atr[0])))
                print("--------------------!!!--------------------")

            elif ((ppo[0]-ppo[1]) >= min_ppo_change*0.7) and (ppo[0]-ppo[1] > ppo[1]-ppo[2]) and ((cci[0]-cci[1]) >= min_cci_change*0.7) and (cci[0]-cci[1] > cci[1]-cci[2]):
                print("--------------------!!!--------------------")
                print(stock+": about to show LONG signal")
                print("--------------------!!!--------------------")

        else:
            print(stock+": kein Signal")


    elif ema_short[0] < ema_long[0]:

        #Kommt CCI aus Long-Trend und ist jetzt neutral/short?
        for i in range(1,3):
            if (cci[0] < 100) and (cci[i] > 100):
                cci_reversal = True
                print("CCI Reversal")
                break

        #wenn CCI im Shorttrend oder Reversal aus 100
        if (cci[0] <= -100) or (cci_reversal):

            #Wenn PPO und CCI fallen (mindestens um X) + PPO-Momentum -> PPO fällt stärker als am Vortag
            if ((ppo[1]-ppo[0]) >= min_ppo_change) and (ppo[1]-ppo[0] > ppo[2]-ppo[1]) and ((cci[1]-cci[0]) >= min_cci_change) and (cci[1]-cci[0] > cci[2]-cci[1]):

                print("--------------------!!!--------------------")
                print("GO SHORT "+stock+" at "+str(stock_data["close"][0]))
                print("Stop Loss 2D High - 1 ATR: "+str(max(stock_data["high"][0], stock_data["high"][1], stock_data["high"][2])+atr[0]))
                print("Stop Loss 2 ATR: "+str(stock_data["high"][0]+(2*atr[0])))
                print("--------------------!!!--------------------")

            elif ((ppo[1]-ppo[0]) >= min_ppo_change*0.7) and (ppo[1]-ppo[0] > ppo[2]-ppo[1]) and ((cci[1]-cci[0]) >= min_cci_change*0.7) and (cci[1]-cci[0] > cci[2]-cci[1]):
                print("--------------------!!!--------------------")
                print(stock+": about to show SHORT signal")
                print("--------------------!!!--------------------")

        else:
            print(stock+": kein Signal")
