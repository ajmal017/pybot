import requests
import json
from time import sleep
import random
from datetime import datetime, timedelta

def get_stock_data_wotd(stock):
    trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0, "currency" : "XXX"}
    wechselkurs = 1.00
    stock_data = []
    no_data = False

    keys = ["elcWQss9HzmuSGhiaYo3dkxR1Dl2gwPEfoau4vNutSwp4RxNDmzZ1ZIBheSk",
"F4M1mbiAPgYF2DIq069wNRhQpYZOFJWKwrvFC2AGBAF0VzutLmm9ESF5WVNp",
"A3fPSXJ7NdydUTW0x6x6mHiUc33CW7NZU7ZoAskF6Hqe4WC2TinRWVQrc9Sx",
"cqjMCVkYU7S79Av4Cua2UppHJk9SlURExfquHdx509nJGCOabUbm6yqIwZ1v",
"dCnmxq7wmGSWrgdbU0zUeAvflvqNE2n9Cc9t4K3iNp1bpi6b2Y7wbaHy92uA",
"Aw17HEYM2AXfV8iqxTb4H93ldtF1YfOAEGEX0u8FxSeEGtLoDY4WO7h9HlwU",
"9ui6I97ecmousE1XJ2nDHMsNztyia9fpSXgobRRPll4jGhqDSL260XiGXYPg",
"w6r2Fz0FiNTbKCJ8URlMI6svDvEVAUFr2gpvpgUN0TRvQdYLUK13T0QASoYW",
"cCz2Xmvobo7nERrfvqaAhPwkYlr8Lb3LgoGq9lUkRZvDA9vLZ0jMJchTBbmH",
"KsUfOdaoCev8ScIlGCPJ4Z1vhHQsAd8q4SQDXYlh12enRK86cacB9QpLrdGK"]

    dt = datetime.today() - timedelta(days=300)
    date = dt.strftime('%Y-%m-%d')
    #date = '2015-01-01'

    for i in range(len(keys)):
        key = keys[i]
        url = "https://www.worldtradingdata.com/api/v1/stock?symbol="+stock+"&api_token="+key
        resp = requests.get(url)

        if "data" in resp.json():

            if resp.json()["data"][0]["currency"] != "EUR":
                wechselkurs = 1#float(get_wechselkurs(resp.json()["data"][0]["currency"]))

            trading_day["date"] = resp.json()["data"][0]["last_trade_time"][:10]

            trading_day["open"] = float(resp.json()["data"][0]["price_open"])*wechselkurs
            trading_day["high"] = float(resp.json()["data"][0]["day_high"])*wechselkurs
            trading_day["low"] = float(resp.json()["data"][0]["day_low"])*wechselkurs
            trading_day["close"] = float(resp.json()["data"][0]["price"])*wechselkurs
            trading_day["volume"] = float(resp.json()["data"][0]["volume"])

            stock_data.append(trading_day)


            url = "https://www.worldtradingdata.com/api/v1/history?symbol="+stock+"&date_from="+date+"&sort=newest&api_token="+key
            resp = requests.get(url)

            if "history" in resp.json() and len(resp.json()["history"]) > 100:

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
        else:
            print("NO DATA!")

    trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}
    stock_data.append(trading_day)
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

def get_wechselkurs(currency):

    dt = datetime.today()
    date = dt.strftime('%Y-%m-%d-%H')

    wechselkurs = 0

    filename = currency + '.txt'


    f = open(filename, 'a')
    f.close()


    with open(filename, 'r') as f:
        for l in f:
            values = l.split(',')
            if values[0] == date:
                wechselkurs = values[1]
            else:

                keys = ["ADHJFQ0PWWESDOFN","MIPDLAHG0TM780KQ","3A745MIJF40Y96BD","PH163RG7NX7HNVS6","50RLUICECDBVL2C5","S0SUWFRW73KGR4L3","YEGWN1N5CCIKUFA4","CGEZJ7R0RH2LSP2O","JMWK5GAVCQE51BOY","8IKZF486MAFUY8PA","J4R0HIQM39MLEL4P","V8ORD946P5RZOFXV","IG34PJVZ2WWKKPJ6","F9P304S1097CBAR8","F04OPCSNNE3WWIRJ","9KYAVL1CCIZQIDNR","PQG9832OUK0RGZOO","0AYYDZX31BDLE158","23HWNCSDM62JR9XF","QDWK1SULIUTSAAFT","NSNF2E09AOJ0QWM4","YARI43A0R5C0HKAH"]
                key = random.choice(keys)

                url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency="+currency+"&to_currency=EUR&apikey=" + key
                resp = requests.get(url)

                if "Realtime Currency Exchange Rate" in resp.json():
                    wechselkurs = resp.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

                    line = date + ',' + wechselkurs

                    with open(filename, 'w') as f:
                        f.write(line)



    return wechselkurs
