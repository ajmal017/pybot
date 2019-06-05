from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import requests
import re
from datetime import time
from  HMA_strat import check_signal
from sl_rechner import get_sl
from kursdaten import get_stock_data

g_bot_id = '802108543:AAFi_gBASTxGhn0oDwLsG74AN9vzg4Rsr3M'
g_mychat_id = 640106465

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def wl_signals(bot):

    with open('WL.txt', 'r') as f:
        for l in f:
            line = l

    wl = line.split(',')

    for i in range(len(wl)):
        output = []
        output = check_signal(wl[i])

        for k in range(len(output)):
            bot.send_message(chat_id = g_mychat_id, text = output[k])

def get_stops(bot):

    with open('PF.txt', 'r') as f:
        for l in f:
            line = l

    pf = line.split(';')

    for i in range(len(pf)):
        trade = []
        trade = pf[i].split(',')

        output = []
        output = get_sl(trade[0], trade[1], float(trade[3]))

        for k in range(len(output)):
            bot.send_message(chat_id = g_mychat_id, text = output[k])


def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def signals(bot, update, args):

    if len(args) > 0:
        for i in range(len(args)):
            output = []
            output = check_signal(args[i])

            chat_id = update.message.chat_id

            for k in range(len(output)):
                bot.send_message(chat_id = chat_id, text = output[k])
    else:
        wl_signals(bot)

def stops(bot, update, args):

    if len(args) > 0:
        if len(args) != 3:
            bot.send_message(chat_id = chat_id, text = 'Symbol Datum EK')
        else:
            for i in range(len(args)):
                output = []
                output = get_sl(args[0], args[1], args[2])

                chat_id = update.message.chat_id

                for k in range(len(output)):
                    bot.send_message(chat_id = chat_id, text = output[k])
    else:
        get_stops(bot)

def daily_signals(bot, job):

    bot.send_message(chat_id = g_mychat_id, text = "!!! Signale aus der WL !!!")
    wl_signals(bot)

def daily_stops(bot, job):

    bot.send_message(chat_id = g_mychat_id, text = "!!! Stops zum Portfolio !!!")
    get_stops(bot)

def add_to_wl(bot, update, args):

    line = ""

    with open('WL.txt', 'r') as f:
        for l in f:
            line = l

    wl = line.split(',')

    for i in range(len(args)):

        if args[i] not in wl:
            if (line != "") and  (i < len(args)):
                line = line + ','
            line = line + args[i]

            bot.send_message(chat_id=update.message.chat_id, text=args[i] + " zur WL hinzugefügt!")

        else:
            bot.send_message(chat_id=update.message.chat_id, text=args[i] + " existiert bereits in WL!")

    with open('WL.txt', 'w') as f:
        f.write(line)

def rm_from_wl(bot, update, args):

    line = ""

    with open('WL.txt', 'r') as f:
        for l in f:
            line = l

    wl = line.split(',')

    for i in range(len(args)):

        if args[i] in wl:
            wl.remove(args[i])
            bot.send_message(chat_id=update.message.chat_id, text=args[i] + " von WL entfernt!")
        else:
            bot.send_message(chat_id=update.message.chat_id, text=args[i] + " existiert nicht in WL!")

        line = ""

        for stock in wl:
            if line != "":
                line = line + ','
            line = line + stock

    with open('WL.txt', 'w') as f:
        f.write(line)

def show_wl(bot, update):

    with open('WL.txt', 'r') as f:
        for l in f:
            line = l

    wl = line.split(',')

    bot.send_message(chat_id=update.message.chat_id, text="Aktuelle WL:")

    for stock in wl:
        bot.send_message(chat_id=update.message.chat_id, text=stock)

def buy(bot, update, args):

    if (len(args) != 6):
        bot.send_message(chat_id=update.message.chat_id, text="Symbol Datum Anzahl EK SL TP!")
        return

    line = ""

    with open('PF.txt', 'r') as f:
        for l in f:
            line = l

    trades = line.split(';')

    l_nachkauf = False
    l_trade = ""

    for trade in trades:
        split_trade = trade.split(',')
        if args[0] == split_trade[0]:
            bot.send_message(chat_id=update.message.chat_id, text=args[0] + " Nachkauf!")

            l_trade = split_trade[0] + ','
            l_trade = l_trade + split_trade[1] + ','
            l_trade = l_trade + str(int(split_trade[2]) + int(args[2])) + ',' #Anzahl
            l_trade = l_trade + str(((float(args[3]) * int(args[2])) + (float(split_trade[3]) * int(split_trade[2]))) / (int(split_trade[2]) + int(args[2]))) + ',' #EK
            l_trade = l_trade + str(split_trade[4]) + ',' #SL
            l_trade = l_trade + str(split_trade[5])#TP
            trades.remove(trade)
            l_nachkauf = True

    if not l_nachkauf:
        l_trade = args[0] + ',' + args[1] + ',' + args[2] + ',' + args[3] + ',' + args[4] + ',' + args[5]
        bot.send_message(chat_id=update.message.chat_id, text=args[0] + " Erstkauf!")

    trades.append(l_trade)

    line = ""

    for trade in trades:
        if (line != ""):
            line = line + ';'
        line = line + trade

    with open('PF.txt', 'w') as f:
        f.write(line)


def sell(bot, update, args):

    if len(args) == 2:

        with open('PF.txt', 'r') as f:
            for l in f:
                line = l

        trades = line.split(';')

        l_vorhanden = False

        for trade in trades:
            split_trade = trade.split(',')
            if args[0] == split_trade[0]:
                bot.send_message(chat_id=update.message.chat_id, text=args[0] + " " + args[1] + " von " + split_trade[2] + " Aktien wurden verkauft!")
                trades.remove(trade)
                l_vorhanden = True

        if not l_vorhanden:
            bot.send_message(chat_id=update.message.chat_id, text=args[0] + " konnte im Portfolio nicht gefunden werden!")

        line = ""

        for trade in trades:
            if (line != ""):
                line = line + ';'
            line = line + trade

        with open('PF.txt', 'w') as f:
            f.write(line)

    else:

        bot.send_message(chat_id=update.message.chat_id, text="Aktie Anzahl!")


def show_pf(bot, update):

    with open('PF.txt', 'r') as f:
        for l in f:
            line = l

    pf = line.split(';')

    bot.send_message(chat_id=update.message.chat_id, text="Aktuelles Portfolio:")

    for trade in pf:

        split_trade = trade.split(',')

        stock_data = []
        stock_data = get_stock_data(split_trade[0])
        l_kurs = 0
        l_kurs = stock_data["close"][0]
        l_entwicklung = 0
        l_entwicklung = (l_kurs - float(split_trade[3]))/float(split_trade[3])*100

        l_text = split_trade[0] + '\nAnzahl: ' + str(split_trade[2]) + "\nEK: " + str(split_trade[3]) + "\nakt. Kurs: " + str(l_kurs) + '\nEntwicklung' + str(l_entwicklung) + '%'
        bot.send_message(chat_id=update.message.chat_id, text=l_text)



def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, I'm helping!")

    l_text = "CMD: /signals - DESCR: Check whether Stock or WL has buy-signals"+"\nCMD: /addWL - DESCR: Add a stock to WL"+"\nCMD: /rmWL - DESCR: Remove a stock from WL"+"\nCMD: /showWL - DESCR: Show your WL"+"\nCMD: /buy - DESCR: Adds n stocks to your PF"+"\nCMD: /sell - DESCR: Sells an amount stock from your PF"+"\nCMD: /showPF - DESCR: Show your Portfolio"+"\nCMD: /getSL - DESCR: Gets the current SL to the stocks in your PF or to the stock you choose"

    bot.send_message(chat_id=update.message.chat_id, text=l_text)

    '''
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /signals - DESCR: Check whether Stock or WL has buy-signals")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /addWL - DESCR: Add a stock to WL")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /rmWL - DESCR: Remove a stock from WL")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /showWL - DESCR: Show your WL")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /buy - DESCR: Adds n stocks to your PF")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /sell - DESCR: Sells an amount stock from your PF")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /showPF - DESCR: Show your Portfolio")
    bot.send_message(chat_id=update.message.chat_id, text="CMD: /getSL - DESCR: Gets the current SL to the stocks in your PF or to the stock you choose")
    '''
    '''
    bot.send_message(chat_id=update.message.chat_id, text= )
    bot.send_message(chat_id=update.message.chat_id, text= )
    bot.send_message(chat_id=update.message.chat_id, text= )
    bot.send_message(chat_id=update.message.chat_id, text= )
    bot.send_message(chat_id=update.message.chat_id, text= )
    bot.send_message(chat_id=update.message.chat_id, text= )
    '''



##################################################################################################
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)



'''
def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    updater = Updater(g_bot_id)
    jobq = updater.job_queue
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    updater.idle()

    daily_job = jobq.run_repeating(signals)

if __name__ == '__main__':
    main()


'''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(g_bot_id)
jobq = updater.job_queue

t1 = time(15,20)
t2 = time(9,45)

daily_signals_jobq = jobq.run_daily(daily_signals,t1)
daily_stops_jobq = jobq.run_daily(daily_stops, t2)

dp = updater.dispatcher
dp.add_handler(CommandHandler('bop',bop))
dp.add_handler(CommandHandler('start',start))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(CommandHandler('caps', caps, pass_args=True))
dp.add_handler(CommandHandler('signals', signals, pass_args=True))
dp.add_handler(CommandHandler('addWL', add_to_wl, pass_args=True))
dp.add_handler(CommandHandler('rmWL', rm_from_wl, pass_args=True))
dp.add_handler(CommandHandler('showWL',show_wl))
dp.add_handler(CommandHandler('buy', buy, pass_args=True))
dp.add_handler(CommandHandler('sell', sell, pass_args=True))
dp.add_handler(CommandHandler('showPF', show_pf))
dp.add_handler(CommandHandler('getSL', stops, pass_args=True))

dp.add_handler(CommandHandler('help',help))


updater.start_polling()
updater.idle()
