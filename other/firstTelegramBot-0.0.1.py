from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3

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
   try:
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customer
                    (id int not null primary key, name varchar(50), telegramID varchar(30),reagent int(20) not null DEFAULT 175224774,isAdmin bool not null DEFAULT 0,
                    `payed` INTEGER DEFAULT 0)""")
    a=c.execute("""SELECT * FROM customer WHERE id = ?""",(int(user_ID),))
    a=c.fetchone()
    print(user_ID)
    if bool(a):
        dbconnect.commit()
        c.close()
        return True
    else:
        dbconnect.commit()
        c.close()
        return False
   except Exception(e):
       print('cant check user existent with error: '+str(e))
       
def dropUser(user_ID):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""DELETE FROM customer WHERE id = ?""",(int(userID),))
        return True
    except Exception(e):
       print('cant check user existent with error: '+str(e))
       return False
    


    
def start(bot, update):
 try:
    print('i')
    

    user_ID=update.message.from_user.id
    print('user_ID: '+ str(user_ID))
    
    update.message.reply_text(update.message.from_user.last_name)
    if bool(update.message.from_user.first_name) and bool(update.message.from_user.last_name):
            name=update.message.from_user.first_name + ' ' +update.message.from_user.last_name
    elif bool(update.message.from_user.first_name):
            name=update.message.from_user.first_name
    elif bool(update.message.from_user.last_name):
            name=update.message.from_user.last_name
        
    print('name: '+ str(name))
    telegramID = update.message.from_user.username
    print('telegramID: '+ str(telegramID))
    reagentID = (update.message.text)[7:]
    print('reagentID: '+ str(reagentID))
    txt1=' سلام ' + name +' عزيز '+'\n' + 'از طريق اين ربات ميتوني به فايلهاي روزنامه ها و سايت ديوار به تفکيک مناطق انتخابي خودتون دسترسي داشته باشي'
    txt2='اما به دليل هزينه هاي سنگين طراحي سرور برنامه، تا زماني که 5 نفر را به ربات دعوت نکنيد، ربات براتون فعال نميشه!'
    txt3='براي دعوت از دوستان کافيه /eshterak  رو لمس کني و براي 5 نفر ارسال کني، تا ما ربات رو برات فعال کنيم'
    txt5= 'شما تاکنون 0 نفر را دعوت کرده ايد'
    print('aaa')
    

    
    if(existUser(user_ID)):
               update.message.reply_text('شما پيش از اين عضو سيستم شده ايد، براي دريافت بنر تبليغاتي اختصاصي خودتان /eshterak را لمس کنيد.')
               print('here2')   
    elif bool(reagentID) and not(existUser(user_ID)): 
          try:
            print('شما توسط آي دي با شماره زير معرفي شده ايد:' + str(reagentID))
            #insert new user to data base
            print('here1')
            insert2DB(user_ID,name,telegramID,reagentID,isAdmin='0',payed='0')
            print('ورود اطلاعات موفق بود!')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')
          except Exception(e):
            update.message.reply_text('در ورود اطلاعات به سيستم مشکلي رخ داده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد.') 
            
    elif(not(reagentID) and not(existUser(user_ID))):
          try:
            print('شما توسط کسي معرفي نشده ايد!!!')
            print('dar hale vared kardan be DB.')
            insert2DB(user_ID,name,telegramID,reagent='175224774',isAdmin='0',payed='0')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')
            print('Succussfuly inserted!')
          except Exception(e):
            update.message.reply_text('در ورود اطلاعات به سيستم مشکلي رخ داده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد.') 
 except Exception(e):
     print(e)
            
                


    
def eshterak(bot, update):
    print(str(update.message.from_user.id))
    txt1='تبريک! \n لينک اختصاصي بات شما فعال شد.'
    txt2='جهت معرفی ربات به دوستانتان ،پیام پایین را برایشان ارسال کنید.'
    update.message.reply_text(txt1 +'\n'+txt2 +'\n')
    
    time.sleep(4)
    
    txt3='اين ربات فايلاي روزنامه ها رو هر روز صبح، و آگهي هاي ديوار رو به محض تاييد  شدن براتون ارسال ميکنه، اونم رايگان!!!'
    
    txt6='https://telegram.me/mydivarbot?start='+str(update.message.from_user.id)#update.message.from_user.id
    bot.sendPhoto(str(update.message.from_user.id),photo='http://imgur.com/a/EVVqV',caption='\n' +'\n'+txt3 + '\n'+txt6)
    #update.message.reply_text(txt3 +'\n'+txt4 +'\n'+txt5 + '\n'+txt6)

 
def echo(bot, update):
     update.message.reply_text(update.message.text)
     print('kk')


token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('eshterak', eshterak))
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()









