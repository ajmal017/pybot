import requests
import json
from time import sleep
import random
from kursdaten_wotd import get_stock_data_wotd

def get_stock_data(stock):

    stock_data = []

    no_data = True
    wotd_req = False

    api_keys = ["ADHJFQ0PWWESDOFN","MIPDLAHG0TM780KQ","3A745MIJF40Y96BD","PH163RG7NX7HNVS6","50RLUICECDBVL2C5","S0SUWFRW73KGR4L3","YEGWN1N5CCIKUFA4","CGEZJ7R0RH2LSP2O","JMWK5GAVCQE51BOY","8IKZF486MAFUY8PA","J4R0HIQM39MLEL4P","V8ORD946P5RZOFXV","IG34PJVZ2WWKKPJ6","F9P304S1097CBAR8","F04OPCSNNE3WWIRJ","9KYAVL1CCIZQIDNR","PQG9832OUK0RGZOO","0AYYDZX31BDLE158","23HWNCSDM62JR9XF","QDWK1SULIUTSAAFT","NSNF2E09AOJ0QWM4","YARI43A0R5C0HKAH"]

    key = random.choice(api_keys)

    #get time series data
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stock+"&apikey="+key

    resp = requests.get(url)

    if "Time Series (Daily)" in resp.json():
        no_data = False


    if no_data:

        print(stock+": NO DATA!")
        trading_day = {"date" : "1900-01-01", "open" : 0, "high" : 0, "low" : 0, "close" : 0, "volume" : 0}
        stock_data.append(trading_day)
        return stock_data

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

    return stock_data
