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
        typical_prices.append((stock_data[i]["high"]+stock_data[i]["low"]+stock_data[i]["close"])/3)

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

def get_vcci(stock_data,vcci_length):

    vsma_values = []

    for i in range(1,len(stock_data) - (vcci_length-2)):

        vsma = 0.0000000000

        for k in range(vcci_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data)+k-1 Tagen
            vsma += stock_data[(i*(-1))-k]["volume"]

        vsma = vsma/vcci_length
        vsma_values.append(vsma)

    vsma_values = vsma_values[::-1]
    vcci_values = []
    vcci = 0
    sma_values = get_sma(stock_data, vcci_length)

    for i in range(5):

        moving_avg = 0.0000000000
        abw_ma = 0.0000000000

        abw_ma = abs(stock_data[i]["close"]-sma_values[i])

        vcci = (stock_data[i]["close"]-moving_avg)/(0.015*abw_ma)*stock_data[i]["volume"]/vsma_values[i]
        vcci_values.append(vcci)

    return vcci_values


def get_sma(stock_data, sma_length):

    sma_values = []

    for i in range(1,len(stock_data) - (sma_length-2)):

        sma = 0.0000000000

        for k in range(sma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data)+k-1 Tagen
            sma += stock_data[(i*(-1))-k]["close"]

        sma = sma/sma_length
        sma_values.append(sma)
        #print(sma)

    last_5_smas = [sma_values[-1], sma_values[-2], sma_values[-3], sma_values[-4], sma_values[-5]]

    return last_5_smas


def get_ema(stock_data, ema_length):

    ema = []
    weight = 2 / (ema_length + 1)

    for i in range(1, len(stock_data) - (ema_length-2)):

        sma = 0.0000000000

        for k in range(ema_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis ema_length
            #erstes Ergebnis ist sma von vor len(stock_data)+k-1 Tagen
            sma += stock_data[(i*(-1))-k]["close"]
        sma = sma/ema_length

        if i == 1:
            ema.append((stock_data[(i*(-1)) - ema_length]["close"] - sma) * weight + sma)
        else:
            ema.append((stock_data[(i*(-1)) - ema_length]["close"] - ema[i-2]) * weight + ema[i-2]) # -1 wegen Vortag und -1 weil bei i bei 1 beginnt

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

    for i in range(len(stock_data)+1):

        high_low = 0
        high_close = 0
        low_close = 0

        high_low = stock_data[(i*(-1))]["high"] - stock_data[(i*(-1))]["low"]

        if (i > 1):

            high_close = abs(stock_data[(i*(-1))]["high"] - stock_data[(i*(-1))+1]["close"])
            low_close = abs(stock_data[(i*(-1))]["low"] - stock_data[(i*(-1))+1]["close"])

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

    for i in range(1,len(stock_data) - (wma_length-2)):

        wma = 0.0000

        for k in range(wma_length):
            #Rückwärts durch Preise iterieren
            #[-1] ist letztes Element
            # k ist Iterator bis sma_length
            #erstes Ergebnis ist sma von vor len(stock_data)+k-1 Tagen
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

def get_rsi(stock_data, rsi_length):

    rsi_values = []
    gains = 0
    losses = 0
    rsi = 0

    for i in range(-2, (-1)*(len(stock_data))-1,-1):

        if i >= -1*rsi_length-1:
            if stock_data[i]["close"] - stock_data[i+1]["close"] > 0:
                gains += stock_data[i]["close"] - stock_data[i+1]["close"]
            else:
                losses += stock_data[i+1]["close"] - stock_data[i]["close"]
            if i == -1*rsi_length-1:
                avg_gains = gains/rsi_length
                avg_losses = losses/rsi_length


        elif i < -1*rsi_length-1:

            gains = 0
            losses = 0

            if stock_data[i]["close"] - stock_data[i+1]["close"] > 0:
                gains = stock_data[i]["close"] - stock_data[i+1]["close"]

            else:
                losses = stock_data[i+1]["close"] - stock_data[i]["close"]

            avg_gains = (avg_gains*(rsi_length-1) + gains)/rsi_length
            avg_losses = (avg_losses*(rsi_length-1) + losses)/rsi_length

        if i <= -1*rsi_length-1:

            if avg_losses == 0:
                rsi = 100
            else:
                rsi = 100-(100/(1+(avg_gains/avg_losses)))

            rsi_values.append(rsi)

    rsi_values = rsi_values[::-1]
    return rsi_values
