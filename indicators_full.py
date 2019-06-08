import requests
import json
from math import sqrt, floor
#from math import sqrt



def get_cci(stock_data,cci_length):

    typical_prices = []
    cci_values = []

    for i in range(len(stock_data)):
        typical_prices.append((stock_data[i]["high"]+stock_data[i]["low"]+stock_data[i]["close"])/3)

    for i in range(len(stock_data)-cci_length):

        moving_avg = 0.0000000000
        abw_ma = 0.0000000000

        for k in range(cci_length):
            moving_avg += typical_prices[k+i]
        moving_avg = moving_avg/cci_length

        for k in range(cci_length):
            abw_ma += abs(typical_prices[k+i]-moving_avg)
        abw_ma = abw_ma/cci_length

        cci_values.append((typical_prices[i]-moving_avg)/(0.015*abw_ma))

    return cci_values


def get_sma(stock_data, sma_length):

    sma_values = []

    for i in range(1,len(stock_data) - (sma_length-1)):

        sma = 0.0000000000

        for k in range(sma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            sma += stock_data[(i*(-1))-k]["close"]

        sma = sma/sma_length
        sma_values.append(sma)

    reversed_smas = sma_values[::-1]

    return reversed_smas


def get_ema(stock_data, ema_length):

    ema = []
    weight = 2 / (ema_length + 1)

    for i in range(1, len(stock_data) - (ema_length-1)):

        sma = 0.0000000000

        for k in range(ema_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis ema_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            sma += stock_data[(i*(-1))-k]["close"]
        sma = sma/ema_length

        if i == 1:
            ema.append((stock_data[(i*(-1)) - ema_length]["close"] - sma) * weight + sma)
        else:
            ema.append((stock_data[(i*(-1)) - ema_length]["close"] - ema[i-2]) * weight + ema[i-2]) # -1 wegen Vortag und -1 weil bei i bei 1 beginnt

    reversed_emas = ema[::-1]

    return reversed_emas



def get_ppo(stock_data, ppo_short, ppo_long):

    ppo = []

    sma_short = get_sma(stock_data, ppo_short)
    sma_short = sma_short[:(-1*(ppo_long-ppo_short))]

    sma_long = get_sma(stock_data, ppo_long)

    for i in range(len(sma_short)):
        ppo.append((sma_short[i]-sma_long[i])/sma_long[i]*100)
    return ppo


def get_atr(stock_data, atr_length):

    tr = []
    atr = []

    for i in range(len(stock_data)):

        high_low = 0
        high_close = 0
        low_close = 0

        high_low = stock_data[(i*(-1))]["high"] - stock_data[(i*(-1))]["low"]

        if (i > 1):

            high_close = abs(stock_data[(i*(-1))]["high"] - stock_data[(i*(-1))+1]["close"])
            low_close = abs(stock_data[(i*(-1))]["low"] - stock_data[(i*(-1))+1]["close"])

        tr.append(max(high_low, high_close, low_close))

    for i in range(len(tr)-atr_length-1):

        atr_value = 0

        for k in range(atr_length):

            atr_value += tr[k+i]

        if (i == 0):
            atr_value = atr_value/atr_length
        else:
            atr_value = (atr[-1] * (atr_length - 1) + tr[k+i])/atr_length

        atr.append(atr_value)

    reversed_atrs = atr[::-1]

    return reversed_atrs

def get_wma(stock_data, wma_length):

    wma_values = []

    for i in range(1,len(stock_data) - (wma_length-2)):

        wma = 0.0000

        for k in range(wma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            wma += stock_data[(i*(-1))-k]["close"]*(k+1)

        wma = wma/((wma_length*(wma_length+1))/2)
        wma_values.append(wma)

    reversed_wmas = wma_values[::-1]

    return reversed_wmas

def get_hma(stock_data, hma_length):

    hma_values = []
    wma_diff = []

    wma1 = get_wma(stock_data, round(hma_length/2))
    wma2 = get_wma(stock_data, hma_length)

    for i in range(len(wma2)):
        wma_diff.append({"close" : 2*wma1[i] - wma2[i]})

    hma_values = get_wma(wma_diff, round(sqrt(hma_length)))

    return hma_values
