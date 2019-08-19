from indicators_full import get_atr
from kursdaten import get_stock_data_wotd

def get_sl(symbol):

    output = []

    #get stock data
    stock_data = get_stock_data_wotd(symbol)

    if (stock_data[0]["open"] <= 0) and (stock_data[0]["close"] <= 0):
        output.append("NO DATA")
        return output

    #indikators
    atr = get_atr(stock_data, 14)

    stops_15 = []
    for i in range(15):
        stops_15.append(0)


    for i in range(30, 0, -1):
        stops_15 = stops_15[1:]
        stops_15.append(stock_data[i]["high"]-5*atr_1[i])


    output.append(stock + " aktueller SL: " + str(max(stops_15)))
    output.append("aktueller Kurs: " + str(stock_data[0]["close"]))

    return output
