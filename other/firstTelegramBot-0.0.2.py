from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3
def openDB():
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    return c
def closeDB():
    dbconnect.commit()
    c.close() 
def insert2DB(ID,name,telegramID,reagent,isAdmin,payed):
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customer
                (id int not null primary key, name varchar(50), telegramID varchar(30),reagent int(20) not null DEFAULT 175224774,isAdmin bool not null DEFAULT 0,
                `payed` INTEGER DEFAULT 0)""")
    c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(ID,name,telegramID,reagent,isAdmin,payed))
    dbconnect.commit()
    c.close()    

def existUser(user_ID):
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    a=c.execute("""SELECT * FROM customer WHERE id = ?""",(user_ID,))
    if bool(a.fetchone()[1]):
        dbconnect.commit()
        c.close()
        return True
    else:
        dbconnect.commit()
        c.close()
        return False

def howManyMyUser(chat_id):
   print() 
def start(bot, update):

    reagentID = (update.message.text)[7:]
    user_ID=update.message.from_user.id
    name=update.message.from_user.first_name + ' ' +update.message.from_user.last_name
    telegramID = update.message.from_user.username
    txt1=' سلام ' + update.message.from_user.first_name + ' '+update.message.from_user.last_name +'عزيز'+'\n' + 'از طريق اين ربات ميتوني به فايلهاي روزنامه ها و سايت ديوار به تفکيک مناطق انتخابي خودتون دسترسي داشته باشي'
    txt2='اما به دليل هزينه هاي سنگين طراحي سرور برنامه، تا زماني که 5 نفر را به ربات دعوت نکنيد، ربات براتون فعال نميشه!'
    txt3='براي دعوت از دوستان کافيه /eshterak  رو لمس کني و براي 5 نفر ارسال کني، تا ما ربات رو برات فعال کنيم'
    #txt4=(update.message.text[7:])
    txt5= 'شما تاکنون 0 نفر را دعوت کرده ايد'
    
    try:
        if(bool(existUser(user_ID))):
               update.message.reply_text('شما پيش از اين عضو سيستم شده ايد، براي دريافت بنر تبليغاتي اختصاصي خودتان /eshterak را لمس کنيد.')
               
        elif bool(reagentID) and not(existUser(user_ID)):
            print('شما توسط آي دي با شماره زير معرفي شده ايد:' + str(reagentID))
            #insert new user to data base
            insert2DB(user_ID,name,telegramID,reagentID,isAdmin='0',payed='0')
            print('ورود اطلاعات موفق بود!')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')
            
        elif(not(reagentID) and not(existUser(user_ID))):    
            print('شما توسط کسي معرفي نشده ايد!!!')
            print('dar hale vared kardan be DB.')
            insert2DB(user_ID,name,telegramID,reagent='175224774',isAdmin='0',payed='0')
            print('Succussfuly inserted!')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')   
    except Exception as e:
        print("can't access to DB, Error: "+str(e))
        


    

    
    
    #print(str(update.message.text)[7:])

    
def eshterak(bot, update):
    txt1='تبريک! \n لينک اختصاصي بات شما فعال شد.'
    txt2='جهت معرفی ربات به دوستانتان ،پیام پایین را برایشان ارسال کنید.'
    update.message.reply_text(txt1 +'\n'+txt2 +'\n')
    
    time.sleep(4)
    
    txt3='اين ربات فايلاي روزنامه ها رو هر روز صبح، و آگهي هاي ديوار رو به محض تاييد  شدن براتون ارسال ميکنه، اونم رايگان!!!'
    
    txt6='https://telegram.me/mydivarbot?start='+str(update.message.from_user.id)#update.message.from_user.id
    bot.sendPhoto('175224774',photo='http://imgur.com/a/EVVqV',caption='\n' +'\n'+txt3 + '\n'+txt6)
    #update.message.reply_text(txt3 +'\n'+txt4 +'\n'+txt5 + '\n'+txt6)
def ozv(bot, update):
    #update.message.reply_text('hi')
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    a=c.execute("""SELECT id,telegramID
                          FROM customer
                          WHERE reagent=?""",(update.message.from_user.id,))
    rows = a.fetchall()
    i=0
    for row in rows:
        i+=1
        update.message.reply_text(row)
    print(i)
    #update.message.reply_text('Ok') 
    dbconnect.commit()
    c.close() 
    update.message.reply_text(' شما تا کنون '  +str(i)+ ' نفر را عضو کرده ايد، ليست افرادي که عضو کرده اين را در زير مشاهده کنيد')
 
def echo(bot, update):
     update.message.reply_text(update.message.text)


token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('eshterak', eshterak))
updater.dispatcher.add_handler(CommandHandler('ozv', ozv))

updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()









