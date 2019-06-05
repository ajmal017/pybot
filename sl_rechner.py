from indicators_full import get_atr, get_sma
from kursdaten_wotd import get_stock_data_wotd


def get_sl(symbol, date, ek):

    output = []

    #get stock data
    stock_data = get_stock_data_wotd(symbol)

    if (stock_data["open"][0] <= 0) and (stock_data["close"][0] <= 0):
        output.append("NO DATA")
        return output

    #indikators
    atr = get_atr(stock_data, 14)
    sma = get_sma(stock_data, 50)

    #get pos of buy date
    date_index = 0

    last_high = 0
    trade = {"EK" : ek, "SL" : 0, "TP": 0, "Anzahl" : 0}

    for i in range(len(stock_data["date"])):
        if (stock_data["date"][i] == date):
            date_index = i
            trade["SL"] = ek - 2.5*atr[i]
            output.append("initialer SL: " + str(trade["SL"]))
            trade["TP"] = ek + 2.5*atr[i]
            output.append("initialer TP: " + str(trade["TP"]))
            break

    output.append("---------" + symbol + "----------")

    #output.append(date_index)

    for i in range(date_index, -1, -1):

        if last_high < stock_data["high"][i]:
            last_high = stock_data["high"][i]

        if (trade["TP"] < last_high - 3*atr[i]):
            trade["TP"] = last_high - 3*atr[i]

        if (stock_data["low"][i] < trade["SL"]):

            output.append(stock_data["date"][i] + " - SL hit - Sold at " + str(trade["SL"]))
            return output

        #output.append(stock_data["date"][i] + ' ' + str(stock_data["high"][i]) + str(i))

        if (trade["TP"] > 0) and (stock_data["high"][i] > trade["TP"]) and trade["SL"] < trade["EK"]:

            trade["SL"] = trade["EK"]
            output.append(str(stock_data["date"][i]) + " - TP überschritten -> Anpassung SL auf EK: " + str(trade["SL"]))

        if  (stock_data["low"][i] < trade["TP"]) and trade["SL"] > trade["EK"]: #SL > EK damit Gewinnmitnahme erst im Profit

            #output.append(stock_data["date"][i] + " - Gewinnmitnahme 50% verkauft (3ATR)")
            #output.append("TP = 0")
            trade["TP"] = 0

        if ((sma[i] - 1.5 * atr[i]) > trade["SL"]) and stock_data["high"][i] > (sma[i] - 1.5 * atr[i]):

            trade["SL"] = (sma[i] - 1.5 * atr[i])
            #output.append(stock_data["date"][i] + " - Anpassung SL auf SMA50: " + str(trade["SL"]))

    output.append("aktueller SL: " + str(trade["SL"]))
    output.append("aktueller TP: " + str(trade["TP"]))
    output.append("letzter Close: " + str(stock_data["close"][0]))

    return output
