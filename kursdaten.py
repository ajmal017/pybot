import requests
import json
from time import sleep
import random
from datetime import datetime, timedelta

def get_stock_data_wotd(stock):
    trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}
    stock_data = []
    no_data = True

    keys = ["wq5pGbL5D7afdTjXIJuYKPHGZchgsDsDyHGpxHPRsblEWHKoccnavQWdFGHq","dCnmxq7wmGSWrgdbU0zUeAvflvqNE2n9Cc9t4K3iNp1bpi6b2Y7wbaHy92uA","QX5Y9J1tkhFrIF91ADrkfzBznag2NcSjSKABpcVuUV1oHa4IpvBN9yLUmoQV"]
    key = random.choice(keys)

    dt = datetime.today() - timedelta(days=200)
    date = dt.strftime('%Y-%m-%d')
    #date = '2015-01-01'

    url = "https://www.worldtradingdata.com/api/v1/stock?symbol="+stock+"&api_token="+key
    resp = requests.get(url)

    if "data" in resp.json():

    		trading_day["date"] = resp.json()["data"][0]["last_trade_time"][:10]

    		trading_day["open"] = float(resp.json()["data"][0]["price_open"])
    		trading_day["high"] = float(resp.json()["data"][0]["day_high"])
    		trading_day["low"] = float(resp.json()["data"][0]["day_low"])
    		trading_day["close"] = float(resp.json()["data"][0]["price"])
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
            stock_data[0]["open"] = float(resp.json()["history"][date]["open"])
            stock_data[0]["high"] = float(resp.json()["history"][date]["high"])
            stock_data[0]["low"] = float(resp.json()["history"][date]["low"])
            stock_data[0]["close"] = float(resp.json()["history"][date]["close"])
            stock_data[0]["volume"] = float(resp.json()["history"][date]["volume"])

        else:
            trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}

            trading_day["date"] = date
            trading_day["open"] = float(resp.json()["history"][date]["open"])
            trading_day["high"] = float(resp.json()["history"][date]["high"])
            trading_day["low"] = float(resp.json()["history"][date]["low"])
            trading_day["close"] = float(resp.json()["history"][date]["close"])
            trading_day["volume"] = float(resp.json()["history"][date]["volume"])

            stock_data.append(trading_day)

    stock_data = sorted(stock_data, key = lambda i: i['date'],reverse=True)


    return stock_data


def get_stock_data(stock):

    stock_data = []

    no_data = True

    api_keys = ["ADHJFQ0PWWESDOFN","MIPDLAHG0TM780KQ","3A745MIJF40Y96BD","PH163RG7NX7HNVS6","50RLUICECDBVL2C5","S0SUWFRW73KGR4L3","YEGWN1N5CCIKUFA4","CGEZJ7R0RH2LSP2O","JMWK5GAVCQE51BOY","8IKZF486MAFUY8PA","J4R0HIQM39MLEL4P","V8ORD946P5RZOFXV","IG34PJVZ2WWKKPJ6","F9P304S1097CBAR8","F04OPCSNNE3WWIRJ","9KYAVL1CCIZQIDNR","PQG9832OUK0RGZOO","0AYYDZX31BDLE158","23HWNCSDM62JR9XF","QDWK1SULIUTSAAFT","NSNF2E09AOJ0QWM4","YARI43A0R5C0HKAH"]

    key = random.choice(api_keys)

    #get time series data
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stock+"&apikey="+key+"&outputsize=full"

    resp = requests.get(url)

    if "Time Series (Daily)" in resp.json():
        no_data = False


    if no_data:

        print(stock+": NO DATA!")
        trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}
        stock_data.append(trading_day)
        return stock_data

    i = 0

    for ts in resp.json()["Time Series (Daily)"]:

        date = str(ts)

        trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}

        trading_day["date"] = date
        trading_day["open"] = float(resp.json()["Time Series (Daily)"][date]["1. open"])
        trading_day["high"] = float(resp.json()["Time Series (Daily)"][date]["2. high"])
        trading_day["low"] = float(resp.json()["Time Series (Daily)"][date]["3. low"])
        trading_day["close"] = float(resp.json()["Time Series (Daily)"][date]["4. close"])
        trading_day["volume"] = float(resp.json()["Time Series (Daily)"][date]["5. volume"])

        stock_data.append(trading_day)

        if i == 200:
            return stock_data

        i+=1

    return stock_data
