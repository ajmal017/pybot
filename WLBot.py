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
    item = {"symbol" : "dummy", "earnings" : "1900-01-01", "timer" : "N"}
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

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        bot.send_message(chat_id=update.message.chat_id, text="Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"] + " Timer: " + str(stock["timer"]))
        count += 1

    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " Werte")

def getNew(bot, update):
    count = 0

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["timer"] == "N":
            bot.send_message(chat_id=update.message.chat_id, text="Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"])
            count += 1

    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " neue Werte")

def getWL(bot, update):
    count = 0

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["timer"] == "0":
            bot.send_message(chat_id=update.message.chat_id, text="Symbol: " + stock["symbol"] + " Earnings: " + stock["earnings"])
            count += 1

    bot.send_message(chat_id=update.message.chat_id, text="Insgesamt " + str(count) + " Werte")

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

    if len(args) == 2:
        with open('Watchlist.txt', 'r') as f:
            json_file = json.load(f)

        found = False

        for k in range(len(json_file["WL"])):
            if args[0] == json_file["WL"][k]["symbol"]:
                found = True
                json_file["WL"][k]["earnings"] = args[1]
                bot.send_message(chat_id=update.message.chat_id, text="Earnings von " + args[0] + " auf " + str(args[1]) + " gesetzt.")

        if found:
            with open('Watchlist.txt', 'w') as f:
                json.dump(json_file, f)
        else:
            bot.send_message(chat_id=update.message.chat_id, text= args[0] + " nicht in WL gefunden!")

    else:
        bot.send_message(chat_id=update.message.chat_id, text="ARGS: Symbol Timer")


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

    url = "https://finviz.com/quote.ashx?t="+stock
    try:
        with urllib.request.urlopen(url) as response:
           html = response.read()
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
           year = str(datetime.today().year)
           earnings = day+"."+month+"."+year+" "+when
    except:
        earnings = "1900-01-01"

    return earnings

def earningsInfoJob(bot,job):
    earningsInfo(bot)

def earningsInfo(bot):

    dt = datetime.today() + timedelta(days=6)

    bot.send_message(chat_id=g_mychat_id, text="Earnings vom " + datetime.today().strftime('%d.%m.%Y') + " bis " + dt.strftime('%d.%m.%Y'))
    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        earnings = datetime.strptime(stock["earnings"][:-4], '%d.%m.%Y')
        if earnings <= dt and earnings >= datetime.today():
            bot.send_message(chat_id=g_mychat_id, text=stock["symbol"] + " - Earnings am " + stock["earnings"])

def updateEarnings(bot, job):

    i = 0

    with open('Watchlist.txt', 'r') as f:
        json_file = json.load(f)

    for stock in json_file["WL"]:
        if stock["earnings"] == "1900-01-01" or datetime.strptime(stock["earnings"][:-4], '%d.%m.%Y') < datetime.today() - timedelta(days=60):
            earnings = getEarnings(stock["symbol"])
            if earnings != "1900-01-01" and earnings == stock["earnings"]:
                del json_file["WL"][i]
                json_file["WL"].append(stock)
            elif earnings != "1900-01-01":
                json_file["WL"][i]["earnings"] = earnings
            else:
                bot.send_message(chat_id=g_mychat_id, text=stock["symbol"] + " Earningsupdate notwendig!")
            i += 1
        if i == 15:
            break
        sleep(60)

    with open('Watchlist.txt', 'w') as f:
        json.dump(json_file, f)





def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(g_bot_id)
jobq = updater.job_queue

t1 = time(6,30)

decrTimer_jobq = jobq.run_daily(decrTimer,t1)
earningsInfo_jobq = jobq.run_daily(earningsInfoJob,t1)

updateEarnings_jobq = jobq.run_repeating(updateEarnings,360)


dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, echo))

dp.add_handler(CommandHandler('add', add, pass_args=True))
dp.add_handler(CommandHandler('rm', rm, pass_args=True))
dp.add_handler(CommandHandler('backup', backup))
dp.add_handler(CommandHandler('getAll', getAll))
dp.add_handler(CommandHandler('getNew', getNew))
dp.add_handler(CommandHandler('getWL', getWL))
dp.add_handler(CommandHandler('setTimer', setTimer, pass_args=True))
dp.add_handler(CommandHandler('decrTimer', decrTimer))
dp.add_handler(CommandHandler('getEarnings', getEarnings, pass_args=True))
dp.add_handler(CommandHandler('earningsInfo', earningsInfo))
dp.add_handler(CommandHandler('updateEarnings', updateEarnings))


updater.start_polling()
updater.idle()
