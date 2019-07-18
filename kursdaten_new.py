import requests
import json
from time import sleep
import random
from datetime import datetime, timedelta

def get_stock_data_wotd(stock):
    trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0, "currency" : "XXX"}
    wechselkurs = 1.00
    stock_data = []
    no_data = True

    keys = ["dCnmxq7wmGSWrgdbU0zUeAvflvqNE2n9Cc9t4K3iNp1bpi6b2Y7wbaHy92uA", "Aw17HEYM2AXfV8iqxTb4H93ldtF1YfOAEGEX0u8FxSeEGtLoDY4WO7h9HlwU","Km4QI7U5gK1lgezFhp09lJAr043IHwM48Pt4qTpC3nihaErH7M63EuZ3jlQj", "O28wlEMmh7y2GkHtiNRnRbsAFVkhsRf1UzteC6gxrmO3KlalxCaVkiKPaBDn"]
    key = random.choice(keys)

    dt = datetime.today() - timedelta(days=200)
    date = dt.strftime('%Y-%m-%d')
    #date = '2015-01-01'

    url = "https://www.worldtradingdata.com/api/v1/stock?symbol="+stock+"&api_token="+key
    resp = requests.get(url)

    if "data" in resp.json():

        if resp.json()["data"][0]["currency"] != "EUR":
            wechselkurs = float(get_wechselkurs(resp.json()["data"][0]["currency"]))

        trading_day["date"] = resp.json()["data"][0]["last_trade_time"][:10]

        trading_day["open"] = float(resp.json()["data"][0]["price_open"])*wechselkurs
        trading_day["high"] = float(resp.json()["data"][0]["day_high"])*wechselkurs
        trading_day["low"] = float(resp.json()["data"][0]["day_low"])*wechselkurs
        trading_day["close"] = float(resp.json()["data"][0]["price"])*wechselkurs
        trading_day["volume"] = float(resp.json()["data"][0]["volume"])

        stock_data.append(trading_day)

    else:
        return get_stock_data(stock)


    url = "https://www.worldtradingdata.com/api/v1/history?symbol="+stock+"&date_from="+date+"&sort=newest&api_token="+key
    resp = requests.get(url)

    if "history" in resp.json() and len(resp.json()["history"]) > 100:
        no_data = False

    if no_data:
        print(stock+": NO DATA!")

    for ts in resp.json()["history"]:

        date = str(ts)

        if str(stock_data[0]["date"]) == str(date):
            stock_data[0]["open"] = float(resp.json()["history"][date]["open"])*wechselkurs
            stock_data[0]["high"] = float(resp.json()["history"][date]["high"])*wechselkurs
            stock_data[0]["low"] = float(resp.json()["history"][date]["low"])*wechselkurs
            stock_data[0]["close"] = float(resp.json()["history"][date]["close"])*wechselkurs
            stock_data[0]["volume"] = float(resp.json()["history"][date]["volume"])

        else:
            trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}

            trading_day["date"] = date
            trading_day["open"] = float(resp.json()["history"][date]["open"])*wechselkurs
            trading_day["high"] = float(resp.json()["history"][date]["high"])*wechselkurs
            trading_day["low"] = float(resp.json()["history"][date]["low"])*wechselkurs
            trading_day["close"] = float(resp.json()["history"][date]["close"])*wechselkurs
            trading_day["volume"] = float(resp.json()["history"][date]["volume"])

            stock_data.append(trading_day)

    stock_data = sorted(stock_data, key = lambda i: i['date'],reverse=True)


    return stock_data
