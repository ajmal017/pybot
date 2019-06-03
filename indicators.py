import requests
import json
from math import sqrt


def get_indicator(stock, indicator, length):

    indicator_values = []

    if indicator != "EMA":
        api_url = "https://www.alphavantage.co/query?function="+indicator+"&symbol="+stock+"&interval=daily&time_period="+str(length)+"&apikey=S0SUWFRW73KGR4L3"
    elif indicator == "EMA":
        api_url = "https://www.alphavantage.co/query?function=EMA&symbol="+stock+"&interval=daily&time_period="+str(length)+"&series_type=close&apikey=S0SUWFRW73KGR4L3"

    resp = requests.get(api_url)

    i = 0

    for ts in resp.json()["Technical Analysis: "+indicator]:

            date = str(ts)

            indicator_values.append(float(resp.json()["Technical Analysis: "+indicator][date][indicator]))

            i+=1

            if i == 5:
                break

    return indicator_values


def get_cci(stock_data,cci_length):

    typical_prices = []
    cci_values = []

    for i in range(cci_length+5):
        typical_prices.append((stock_data["high"][i]+stock_data["low"][i]+stock_data["close"][i])/3)

    for i in range(5):

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

    for i in range(1,len(stock_data["close"]) - (sma_length-2)):

        sma = 0.0000000000

        for k in range(sma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            sma += stock_data["close"][(i*(-1))-k]

        sma = sma/sma_length
        sma_values.append(sma)
        #print(sma)

    last_5_smas = [sma_values[-1], sma_values[-2], sma_values[-3], sma_values[-4], sma_values[-5]]

    return last_5_smas


def get_ema(stock_data, ema_length):

    ema = []
    weight = 2 / (ema_length + 1)

    for i in range(1, len(stock_data["close"]) - (ema_length-1)):

        sma = 0.0000000000

        for k in range(ema_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis ema_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            sma += stock_data["close"][(i*(-1))-k]
        sma = sma/ema_length

        if i == 1:
            ema.append((stock_data["close"][(i*(-1)) - ema_length] - sma) * weight + sma)
        else:
            ema.append((stock_data["close"][(i*(-1)) - ema_length] - ema[i-2]) * weight + ema[i-2]) # -1 wegen Vortag und -1 weil bei i bei 1 beginnt

    last_5_emas = [ema[-1], ema[-2], ema[-3], ema[-4], ema[-5]]

    return last_5_emas



def get_ppo(stock_data, ppo_short, ppo_long):

    ppo = []

    sma_short = get_sma(stock_data, ppo_short)
    sma_long = get_sma(stock_data, ppo_long)

    for i in range(5):
        ppo.append((sma_short[i]-sma_long[i])/sma_long[i]*100)

    return ppo


def get_atr(stock_data, atr_length):

    tr = []
    atr = []

    for i in range(1, len(stock_data["open"])+1):

        high_low = 0
        high_close = 0
        low_close = 0

        high_low = stock_data["high"][(i*(-1))] - stock_data["low"][(i*(-1))]

        if (i > 1):

            high_close = abs(stock_data["high"][(i*(-1))] - stock_data["close"][(i*(-1))+1])
            low_close = abs(stock_data["low"][(i*(-1))] - stock_data["close"][(i*(-1))+1])

        tr.append(max(high_low, high_close, low_close))

    for i in range(len(tr)-atr_length+1):

        atr_value = 0

        for k in range(atr_length):

            atr_value += tr[k+i]

            if (i == 0):
                atr_value = atr_value/atr_length
            else:
                atr_value = (atr[-1] * (atr_length - 1) + tr[k+i])/atr_length

        atr.append(atr_value)

    last_5_atr = [atr[-1], atr[-2], atr[-3], atr[-4], atr[-5]]

    return last_5_atr

def get_wma(stock_data, wma_length):

    wma_values = []

    for i in range(1,len(stock_data["close"]) - (wma_length-2)):

        wma = 0.0000

        for k in range(wma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data["close"])+k-1 Tagen
            wma += stock_data["close"][(i*(-1))-k]*(k+1)

        wma = wma/((wma_length*(wma_length+1))/2)
        wma_values.append(wma)

    reversed_wmas = wma_values[::-1]

    return reversed_wmas

def get_hma(stock_data, hma_length):

    hma_values = []
    wma_diff = {"close":[]}

    wma1 = get_wma(stock_data, round(hma_length/2))
    wma2 = get_wma(stock_data, hma_length)

    for i in range(len(wma2)):
        wma_diff["close"].append(2*wma1[i] - wma2[i])

    hma_values = get_wma(wma_diff, round(sqrt(hma_length)))

    return hma_values
