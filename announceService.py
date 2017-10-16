import requests
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#_________________________________________________________________________________________________________________________________________________



def insert2DB(ID,regDate):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS customer
                    (ID int not null primary key,`keyWords` TEXT,`regDate` TEXT')""")
        c.execute("""INSERT INTO customer (id,regDate) VALUES (?,?)""",
                  (ID,regDate))
        dbconnect.commit()
        c.close()
    except Exception as e:
        print(str(e))


def start(bot, update):
        try:
            update.message.reply_text('hi')
            user_ID=update.message.from_user.id
            txt1=' سلام '
            name=" "
            if(update.message.from_user.first_name):
                    name += str(update.message.from_user.first_name)
            if(update.message.from_user.last_name):
                    name+=' '+ str(update.message.from_user.last_name)
            txt1+=name + ' \n'

            txt2=('کليد زير را فشار دهيد تا بتوانيد آگهي مورد نظرتان را پيدا کنيد.')

            insert2DB(user_ID,name,telegramID,reagent='175224774',isAdmin='0',payed='0',payedThisMount='0',regDate=date.today())
            print('Succussfuly inserted!')
            update.message.reply_text(txt1 +'\n')
            update.message.reply_text(txt2)
        except Exception as e:
            print("can't access to DB, Error: "+str(e))






token='430760169:AAGuiBv7XpPQS2QE4ePYedwXCtLjQKuER2A'
updater = Updater(token)


updater.dispatcher.add_handler(CommandHandler('start', start))








        

#_______________________________________________________________________
updater.start_polling()
updater.idle()
