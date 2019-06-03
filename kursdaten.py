import requests
import json
from time import sleep
import random
from kursdaten_wotd import get_stock_data_wotd

def get_stock_data(stock):

    open = []
    high = []
    low = []
    close = []
    volume = []
    datum = []

    stock_data = {}

    no_data = True
    wotd_req = False

    api_keys = ["ADHJFQ0PWWESDOFN","MIPDLAHG0TM780KQ","3A745MIJF40Y96BD","PH163RG7NX7HNVS6","50RLUICECDBVL2C5","S0SUWFRW73KGR4L3","YEGWN1N5CCIKUFA4","CGEZJ7R0RH2LSP2O","JMWK5GAVCQE51BOY","8IKZF486MAFUY8PA","J4R0HIQM39MLEL4P","V8ORD946P5RZOFXV","IG34PJVZ2WWKKPJ6","F9P304S1097CBAR8","F04OPCSNNE3WWIRJ","9KYAVL1CCIZQIDNR","PQG9832OUK0RGZOO","0AYYDZX31BDLE158","23HWNCSDM62JR9XF","QDWK1SULIUTSAAFT","NSNF2E09AOJ0QWM4","YARI43A0R5C0HKAH"]

    for i in range(4):

        key = random.choice(api_keys)

        #get time series data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stock+"&apikey="+key

        resp = requests.get(url)

        if "Time Series (Daily)" in resp.json():
            no_data = False
            break

        else:
            stock_data = get_stock_data_wotd(stock)

        if stock_data["open"][0] != 0:
            no_data = False
            wotd_req = True
            break

        else:
            sleep(10)

    if no_data:

        print(stock+": NO DATA!")

        open.append(float(0))
        high.append(float(0))
        low.append(float(0))
        close.append(float(0))
        volume.append(float(0))

    elif not wotd_req:

        for ts in resp.json()["Time Series (Daily)"]:

            date = str(ts)

            open.append(float(resp.json()["Time Series (Daily)"][date]["1. open"]))
            high.append(float(resp.json()["Time Series (Daily)"][date]["2. high"]))
            low.append(float(resp.json()["Time Series (Daily)"][date]["3. low"]))
            close.append(float(resp.json()["Time Series (Daily)"][date]["4. close"]))
            volume.append(float(resp.json()["Time Series (Daily)"][date]["5. volume"]))
            datum.append(date)

        stock_data["open"] = open
        stock_data["high"] = high
        stock_data["low"] = low
        stock_data["close"] = close
        stock_data["volume"] = volume
        stock_data["date"] = datum

    return stock_data


def get_full_stock_data(stock):

    open = []
    high = []
    low = []
    close = []
    volume = []

    stock_data = {}

    no_data = True
    #wotd_req = False

    api_keys = ["ADHJFQ0PWWESDOFN","MIPDLAHG0TM780KQ","3A745MIJF40Y96BD","PH163RG7NX7HNVS6","50RLUICECDBVL2C5","S0SUWFRW73KGR4L3","YEGWN1N5CCIKUFA4","CGEZJ7R0RH2LSP2O","JMWK5GAVCQE51BOY","8IKZF486MAFUY8PA","J4R0HIQM39MLEL4P","V8ORD946P5RZOFXV","IG34PJVZ2WWKKPJ6","F9P304S1097CBAR8","F04OPCSNNE3WWIRJ","9KYAVL1CCIZQIDNR","PQG9832OUK0RGZOO","0AYYDZX31BDLE158","23HWNCSDM62JR9XF","QDWK1SULIUTSAAFT","NSNF2E09AOJ0QWM4","YARI43A0R5C0HKAH"]

    for i in range(4):

        key = random.choice(api_keys)

        #get time series data
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol="+stock+"&apikey="+key

        resp = requests.get(url)

        if "Time Series (Daily)" in resp.json():
            no_data = False
            break

        else:
            sleep(10)

    if no_data:

        print(stock+": NO DATA!")

        open.append(float(0))
        high.append(float(0))
        low.append(float(0))
        close.append(float(0))
        volume.append(float(0))

    else:

        for ts in resp.json()["Time Series (Daily)"]:

            date = str(ts)

            open.append(float(resp.json()["Time Series (Daily)"][date]["1. open"]))
            high.append(float(resp.json()["Time Series (Daily)"][date]["2. high"]))
            low.append(float(resp.json()["Time Series (Daily)"][date]["3. low"]))
            close.append(float(resp.json()["Time Series (Daily)"][date]["4. close"]))
            volume.append(float(resp.json()["Time Series (Daily)"][date]["5. volume"]))

        stock_data["open"] = open
        stock_data["high"] = high
        stock_data["low"] = low
        stock_data["close"] = close
        stock_data["volume"] = volume

    return stock_data
