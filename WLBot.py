from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import requests
import re
from datetime import time
import json
from time import sleep
import urllib
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timedelta
from proxy_requests import ProxyRequests
import random


g_bot_id = '1009930804:AAEST4BhDyfl_rpYwHlTcZjMhzKKotBWtKs'
g_mychat_id = 640106465



def add(bot, update, args):

    result = {"added" : [] , "existed" : []}

    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text="Nothing to add...")
    else:
        for i in range(len(args)):
            result = add_to_WL(bot, update, args[i], result)
            sleep(1.5)

        bot.send_message(chat_id=update.message.chat_id, text=str(len(result["added"]))+" Werte hinzugefügt " + str(result["added"]))
        bot.send_message(chat_id=update.message.chat_id, text=str(len(result["existed"]))+" Werte existierten bereits " + str(result["existed"]))


def add_to_WL(bot, update, stock, result):


    json_file = {}
    item = {"symbol" : "dummy", "earnings" : "1900-01-01", "timer" : "N", "comment" : ""}
    found = False

    try:
        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

            for i in range(len(json_file["WL"])):
                if stock == json_file["WL"][i]["symbol"]:
                    found = True
                    #bot.send_message(chat_id=update.message.chat_id, text=stock + " existiert bereits in WL!")
                    result["existed"].append(stock)
            if not found:
                item["symbol"] = stock
                #item["earnings"] = getEarnings(stock)
                json_file["WL"].append(item)
                #bot.send_message(chat_id=update.message.chat_id, text=stock + " zur WL hinzugefügt!")
                result["added"].append(stock)

    except:
        item["symbol"] = stock
        #item["earnings"] = getEarnings(stock)
        json_file["WL"] = []
        json_file["WL"].append(item)
        #bot.send_message(chat_id=update.message.chat_id, text=stock + " zur WL hinzugefügt!")
        result["added"].append(stock)


    with open('Watchlist.txt', 'w') as f:
        json.dump(json_file, f)

    return result

def rm(bot, update, args):

    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id, text="Nothing to remove...")

    elif len(args) == 1 and args[0] == "ALL":

        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

        with open('Backup.txt', 'w') as f:
            json.dump(json_file, f)

        with open('Watchlist.txt', 'w') as f:
            f.write("")

        bot.send_message(chat_id=update.message.chat_id, text="Alle Werte entfernt!")

    else:

        count = 0

        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

            for i in range(len(args)):
                k = 0
                for stock in json_file["WL"]:
                    if args[i] == stock["symbol"]:
                        del json_file["WL"][k]
                        bot.send_message(chat_id=update.message.chat_id, text=args[i] + " aus WL entfernt!")
                        count += 1
                    k += 1

        with open('Watchlist.txt', 'w') as f:
            json.dump(json_file, f)

        bot.send_message(chat_id=update.message.chat_id, text=str(count)+" Werte entfernt")

def backup(bot, update):

    json_file = {}

    with open('Backup.txt', 'r') as f:
        json_file = json.load(f)

    with open('Watchlist.txt', 'w') as f:
        json.dump(json_file, f)

    bot.send_message(chat_id=update.message.chat_id, text="Backup wieder hergestellt!")

def getAll(bot, update):
    count = 0
    l_msg = ""
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        l_msg = l_msg + "Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"] + " Timer: " + str(stock["timer"]) + " Kommentar: " + stock["comment"] + "\n"
        count += 1
        if count%20 == 0:
            bot.send_message(chat_id=update.message.chat_id, text=l_msg)
            l_msg = ""

    bot.send_message(chat_id=update.message.chat_id, text=l_msg)
    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " Werte")

def getNew(bot, update):
    count = 0
    l_msg = ""
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["timer"] == "N":
            l_msg = l_msg + "Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"]+"\n"
            count += 1
            if count%20 == 0:
                bot.send_message(chat_id=update.message.chat_id, text=l_msg)
                l_msg = ""

    bot.send_message(chat_id=update.message.chat_id, text=l_msg)
    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " neue Werte")

def getWL(bot, update):
    count = 0
    l_msg = ""
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["timer"] == "0":
            l_msg = l_msg + "Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"] + " Kommentar: " + stock["comment"] +"\n"
            count += 1
            if count%20 == 0:
                bot.send_message(chat_id=update.message.chat_id, text=l_msg)
                l_msg = ""

    bot.send_message(chat_id=update.message.chat_id, text=l_msg)
    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " Werte")

def get(bot, update, args):

    l_msg = ""
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["symbol"] in args:
            l_msg = l_msg + "Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"] + " Timer: " + str(stock["timer"]) + " Kommentar " + stock["comment"]  +"\n"


    bot.send_message(chat_id=update.message.chat_id, text=l_msg)


def setTimer(bot, update, args):

    if len(args) == 2:
        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

        found = False

        for k in range(len(json_file["WL"])):
            if args[0] == json_file["WL"][k]["symbol"]:
                found = True
                json_file["WL"][k]["timer"] = args[1]
                bot.send_message(chat_id=update.message.chat_id, text="Timer von " + args[0] + " auf " + str(args[1]) + " gesetzt.")

        if found:
            with open('Watchlist.txt', 'w') as f:
                json.dump(json_file, f)
        else:
            bot.send_message(chat_id=update.message.chat_id, text= args[0] + " nicht in WL gefunden!")

    else:
        bot.send_message(chat_id=update.message.chat_id, text="ARGS: Symbol Timer")


def setEarnings(bot, update, args):

    if len(args) == 3 or (len(args) == 2 and args[1] == "1900-01-01"):
        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

        found = False

        if len(args) == 2:
            earnings = args[1]
        else:
            earnings = args[1] + " " + args[2]

        for k in range(len(json_file["WL"])):
            if args[0] == json_file["WL"][k]["symbol"]:
                found = True
                json_file["WL"][k]["earnings"] = earnings
                bot.send_message(chat_id=update.message.chat_id, text="Earnings von " + args[0] + " auf " + str(json_file["WL"][k]["earnings"]) + " gesetzt.")

        if found:
            with open('Watchlist.txt', 'w') as f:
                json.dump(json_file, f)
        else:
            bot.send_message(chat_id=update.message.chat_id, text= args[0] + " nicht in WL gefunden!")

    else:
        bot.send_message(chat_id=update.message.chat_id, text="ARGS: Symbol Earnings [AMC/BMO]... / 1900-01-01 ")

def setComment(bot, update, args):

    if len(args) == 2:
        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

        for i in range(len(json_file["WL"])):
            if args[0] == json_file["WL"][i]["symbol"]:
                found = True
                json_file["WL"][i]["comment"] = args[1]
                bot.send_message(chat_id=update.message.chat_id, text="Kommentar von " + args[0] + " auf " + str(json_file["WL"][k]["comment"]) + " gesetzt.")

            if found:
                with open('Watchlist.txt', 'w') as f:
                    json.dump(json_file, f)
                break
        else:
            bot.send_message(chat_id=update.message.chat_id, text= args[0] + " nicht in WL gefunden!")

    else:
        bot.send_message(chat_id=update.message.chat_id, text="ARGS: Symbol  Kommentar in Gänsefüßchen")


def decrTimer(bot, job):

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for k in range(len(json_file["WL"])):
        if json_file["WL"][k]["timer"] not in ["N", "0"]:
            json_file["WL"][k]["timer"] = str(int(json_file["WL"][k]["timer"]) - 1)

    with open('Watchlist.txt', 'w') as f:
        json.dump(json_file, f)

    bot.send_message(chat_id = g_mychat_id, text="Timers decreased...")

def getEarnings(stock):
    try:
        url = "https://finviz.com/quote.ashx?t="+stock

        user_agent_list = [

            'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
            'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
            'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16',
            'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14'

        ]

        request = ProxyRequests(url)
        #request.get()
        user_agent = random.choice(user_agent_list)
        h = {"User-Agent": user_agent}
        request.set_headers(h)
        request.get_with_headers()

        html = str(request)

        soup = BeautifulSoup(html, 'html.parser')
        earnings = soup.contents[36].table.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.b.string
        month = {
        "Jan":"01",
        "Feb":"02",
        "Mar":"03",
        "Apr":"04",
        "May":"05",
        "Jun":"06",
        "Jul":"07",
        "Aug":"08",
        "Sep":"09",
        "Oct":"10",
        "Nov":"11",
        "Dec":"12"
        }[earnings[:3]]
        day = earnings[4:6]
        when = earnings[7:]
        if when not in ["AMC","BMO"]:
            when = "XXX"
        year = str(datetime.today().year)
        earnings = day+"."+month+"."+year+" "+when

        r = None
        return earnings

    except:
        print(stock + " Error beim Scraping! // earnings: " + earnings)
        r = None
        return "1900-01-01"

def earningsInfoJob(bot,job):
    earningsInfo(bot)

def earningsInfo(bot, update):

    dt = datetime.today() + timedelta(days=6)
    l_msg = ""
    l_count = 0

    bot.send_message(chat_id=g_mychat_id, text="Earnings vom " + datetime.today().strftime('%d.%m.%Y') + " bis " + dt.strftime('%d.%m.%Y'))
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["earnings"] != "1900-01-01":
            earnings = datetime.strptime(stock["earnings"][:-4], '%d.%m.%Y')
            if earnings <= dt and earnings >= datetime.today():
                l_msg = l_msg + stock["symbol"] + " - Earnings am " + stock["earnings"] + "\n"
                l_count += 1
                if l_count%20 == 0:
                    bot.send_message(chat_id=g_mychat_id, text=l_msg)
                    l_msg = ""

    bot.send_message(chat_id=g_mychat_id, text=l_msg)

def updateEarnings(bot, update):

    i = 0
    count = 0

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        try:
            if stock["earnings"] == "1900-01-01" or datetime.strptime(stock["earnings"][:-4], '%d.%m.%Y') < datetime.today() - timedelta(days=60):
                earnings = getEarnings(stock["symbol"])
                if earnings != "1900-01-01" and earnings == stock["earnings"]:
                    del json_file["WL"][i]
                    json_file["WL"].append(stock)
                elif earnings != "1900-01-01":
                    json_file["WL"][i]["earnings"] = earnings
                else:
                    bot.send_message(chat_id=g_mychat_id, text=stock["symbol"] + " Earningsupdate notwendig!")
                #count += 1
                sleep(0.5)
            #if count == 12:
                #break
        except:
            print("stockname: " + stock["symbol"] + "earnings 4: " + stock["earnings"][:-4])
            bot.send_message(chat_id=g_mychat_id, text=stock["symbol"] + " Earningsupdate notwendig!")
        i+=1


    with open('Watchlist.txt', 'w') as f:
        json.dump(json_file, f)


def help(bot,update):
    l_msg = ""
    l_msg = l_msg + '/add' + "\n"
    l_msg = l_msg + '/rm' + "\n"
    l_msg = l_msg + '/backup' + "\n"
    l_msg = l_msg + '/getAll' + "\n"
    l_msg = l_msg + '/getNew' + "\n"
    l_msg = l_msg + '/getWL' + "\n"
    l_msg = l_msg + '/get' + "\n"
    l_msg = l_msg + '/setTimer' + "\n"
    l_msg = l_msg + '/setEarnings' + "\n"
    l_msg = l_msg + '/decrTimer' + "\n"
    l_msg = l_msg + '/earningsInfo' + "\n"
    l_msg = l_msg + '/updateEarnings' + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=l_msg)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(g_bot_id)
jobq = updater.job_queue

t1 = time(6,30)

updateEarnings_jobq = jobq.run_daily(updateEarnings,t1)
decrTimer_jobq = jobq.run_daily(decrTimer,t1)
earningsInfo_jobq = jobq.run_daily(earningsInfoJob,t1)

#updateEarnings_jobq = jobq.run_repeating(updateEarnings,3600)


dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, echo))

dp.add_handler(CommandHandler('add', add, pass_args=True))
dp.add_handler(CommandHandler('rm', rm, pass_args=True))
dp.add_handler(CommandHandler('backup', backup))
dp.add_handler(CommandHandler('getAll', getAll))
dp.add_handler(CommandHandler('getNew', getNew))
dp.add_handler(CommandHandler('getWL', getWL))
dp.add_handler(CommandHandler('get', get, pass_args=True))
dp.add_handler(CommandHandler('setTimer', setTimer, pass_args=True))
dp.add_handler(CommandHandler('setEarnings', setEarnings, pass_args=True))
dp.add_handler(CommandHandler('setComment', setComment, pass_args=True))
dp.add_handler(CommandHandler('decrTimer', decrTimer))
dp.add_handler(CommandHandler('earningsInfo', earningsInfo))
dp.add_handler(CommandHandler('updateEarnings', updateEarnings))
dp.add_handler(CommandHandler('help', help))


updater.start_polling()
updater.idle()
