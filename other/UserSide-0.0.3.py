import requests
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#_________________________________________________________________________________________________________________________________________________
#________________________________________________________User Side _______________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________



        
def insert2DB(ID,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS customer
                    (id int not null primary key, name varchar(50), telegramID varchar(30),reagent int(20) not null DEFAULT 175224774,isAdmin bool not null DEFAULT 0,
                    `payed` INTEGER DEFAULT 0,`payedThisMount`	INTEGER DEFAULT 0,`regDate` TEXT,`lastPaymentDate`	TEXT DEFAULT '2016-1-1')""")
        c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate) VALUES (?,?,?,?,?,?,?,?)""",
                  (ID,name,telegramID,reagent,isAdmin,payed,0,regDate))
        dbconnect.commit()
        c.close()
    except Exception as e:
        print(str(e))
def existUser(user_ID):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT * FROM customer WHERE id = ?""",(user_ID,))
        if bool(a.fetchone()):
            dbconnect.commit()
            c.close()
            return True
        else:
            dbconnect.commit()
            c.close()
            return False
    except Exception as e:
        print(str(e))
def start(bot, update):
  
    reagentID = (update.message.text)[7:]
    user_ID=update.message.from_user.id
    txt1=' سلام ' 
    if(update.message.from_user.first_name):
                txt1 += str(update.message.from_user.first_name)
    if(update.message.from_user.last_name):
                txt1+=' '+ str(update.message.from_user.last_name)
    name=txt1 + ' '
    telegramID = update.message.from_user.username
    txt1=' سلام ' + update.message.from_user.first_name + ' '+update.message.from_user.last_name +'عزيز'+'\n' + 'از طريق اين ربات ميتوني به فايلهاي روزنامه ها و سايت ديوار به تفکيک مناطق انتخابي خودتون دسترسي داشته باشي'
    txt2='اما به دليل هزينه هاي سنگين طراحي سرور برنامه، تا زماني که 5 نفر را به ربات دعوت نکنيد، ربات براتون فعال نميشه!'
    txt3='براي دعوت از دوستان کافيه /eshterak  رو لمس کني و براي 5 نفر ارسال کني، تا ما ربات رو برات فعال کنيم'
    #txt4=(update.message.text[7:])
    txt5= 'شما تاکنون 0 نفر را دعوت کرده ايد'
    
    try:
        if(bool(existUser(user_ID))):
               update.message.reply_text('شما پيش از اين عضو سيستم شده ايد، براي دريافت بنر تبليغاتي اختصاصي خودتان /eshterak را لمس کنيد.')
               update.message.reply_text('/commands : دستورات بات')
               
        elif bool(reagentID) and not(existUser(user_ID)):
            print('شما توسط آي دي با شماره زير معرفي شده ايد:' + str(reagentID))
            #insert new user to data base
            insert2DB(user_ID,name,telegramID,reagentID,isAdmin='0',payed='0',payedThisMount='0',regDate=date.today())
            print('ورود اطلاعات موفق بود!')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')
            update.message.reply_text('/commands : دستورات بات')
            
        elif(not(reagentID) and not(existUser(user_ID))):    
            print('شما توسط کسي معرفي نشده ايد!!!')
            print('dar hale vared kardan be DB.')
            insert2DB(user_ID,name,telegramID,reagent='175224774',isAdmin='0',payed='0',payedThisMount='0',regDate=date.today())
            print('Succussfuly inserted!')
            update.message.reply_text(txt1 +'\n'+txt2 +'\n'+txt3 +'\n'+txt5 +'\n')
            update.message.reply_text('/commands : دستورات بات')
    except Exception as e:
        print("can't access to DB, Error: "+str(e))
    viewButtons(bot, update,'start')
    

    

    
def eshterak(bot, update):
    txt1='تبريک! \n لينک اختصاصي بات شما فعال شد.'
    txt2='جهت معرفی ربات به دوستانتان ،پیام پایین را برایشان ارسال کنید.'
    update.message.reply_text(txt1 +'\n'+txt2 +'\n')
    
    time.sleep(4)
    
    txt3='اين ربات فايلاي روزنامه ها رو هر روز صبح، و آگهي هاي ديوار رو به محض تاييد  شدن براتون ارسال ميکنه، اونم رايگان!!!'
    
    txt6='https://telegram.me/mydivarbot?start='+str(update.message.from_user.id)#update.message.from_user.id
    bot.sendPhoto(update.message.from_user.id,photo='http://imgur.com/a/EVVqV',caption='\n' +'\n'+txt3 + '\n'+txt6)
    time.sleep(8)
    update.message.reply_text('/commands : دستورات بات')
    #update.message.reply_text(txt3 +'\n'+txt4 +'\n'+txt5 + '\n'+txt6)
def ozv(bot, update):
    print(update.message.from_user)
    try:
        #update.message.reply_text('hi')
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT id,telegramID FROM customer WHERE reagent = ?""",(update.message.from_user.id,))
        rows = a.fetchall()
        i=0
        for row in rows:
            i+=1
            update.message.reply_text(str(i)+' - ' + str(row))
        print(i)
        #update.message.reply_text('Ok') 
        dbconnect.commit()
        c.close() 
        update.message.reply_text(' شما تا کنون '  +str(i)+ 'نفر را عضو کرده ايد، ليست افرادي که توسط شما عضو شده اند را در بالا مشاهده کنيد.')
        update.message.reply_text('/commands : دستورات بات')
    except Exception as e:
        update.message.reply_text('در اتصال به پايگاه داده مشکلي پيش امده است، لطفا صبور باشيد و چند دقيقه بعد امتحان کنيد.')
        update.message.reply_text('/commands : دستورات بات')
        print(str(e))
        
def activeUsers(bot, update):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT id,telegramID FROM customer WHERE reagent = ? AND payed=1""",(update.message.from_user.id,))
        rows = a.fetchall()
        i=0
        for row in rows:
            i+=1
            update.message.reply_text(str(i)+' - ' + str(row))
        print(i)
        dbconnect.commit()
        c.close()
        txt1= update.message.from_user.first_name + ' '+update.message.from_user.last_name +'عزيز'+'\n' 
        update.message.reply_text(txt1 + ' تا کنون '  +str(i)+ ' نفر از افرادي که شما جذب کرده ايد، از ما خريد داشته اند.')
        update.message.reply_text('/commands : دستورات بات')
    except Exception as e:
        update.message.reply_text('در اتصال به پايگاه داده مشکلي پيش امده است، لطفا صبور باشيد و چند دقيقه بعد امتحان کنيد.')
        update.message.reply_text('/commands : دستورات بات')
        print(str(e))
        
def hi(bot, update):
    try:
        update.message.reply_text('hi')
        time.sleep(120)
        update.message.reply_text('bye')
    except Exception as e:
        update.message.reply_text(str(e))
    
def commands(bot, update):
    txt1='دستورات ربات:\n\n'
    txt2='/eshterak : مشاهده بنر اختصاصيتان جهت ارسال به دوستان \n\n'
    txt3='/ozv : مشاهده ي تمامي افرادي که جذب کرده ايد. \n\n'
    txt4='/activeusers : مشاهده افرادي که توسط شما جذب شده اند و از ما خريد کرده اند. \n\n'
    txt5='/showID دريافت کد کاربري\n\n'
    update.message.reply_text(txt1+txt5+txt3+txt2+txt4)
    #viewButtons(bot, update,'')


def button(bot, update):
    query = update.callback_query
    print(str(query.data))
    if("%s"%query.data=='eshterak'):
        try:
            print('0000')
            eshterak(bot, update)
            print('111')
        except Exception as e:
            print(str(e))
            
def viewButtons(bot, update,s):
    try:
     if (False):
        print('aa')
        keyboard = [[InlineKeyboardButton('مشاهده بنر(دعوت از دوستان)', callback_data='eshterak')],
                    [InlineKeyboardButton('مشاهده تمام افرادي که جذب کرده ايد ', callback_data='/ozv')],
                    [InlineKeyboardButton('مشاهده افرادي که جذب کرده ايد و پرداخت داشته اند', callback_data='/activeusers')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('دستور بعدي را انتخاب کنيد:', reply_markup=reply_markup)

    except:
        update.message.reply_text('در اجراي قسمتی از برنامه مشکلي پيش آمده، لطفا صبور باشيد و پس از چند دقيقه دوباره امتحان کنيد.')

def showId(bot, update):
    txt1= update.message.from_user.first_name + ' '+update.message.from_user.last_name +' عزيز \n' + 'کد کاربري شما \n'
    txt2= update.message.from_user.id
    txt3=' ميباشد. ' 
    update.message.reply_text(txt1)
    update.message.reply_text(txt2)
    update.message.reply_text(txt3)
    time.sleep(5)
    update.message.reply_text('/commands : دستورات بات')

#_________________________________________________________________________________________________________________________________________________
#________________________________________________________Admin Side _______________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________
def extractUserInfo(id):
    print('')
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    a=c.execute("""SELECT * FROM customer WHERE id = ?""",(id,))
    a=a.fetchone()
    id=a[0]
    name=a[1]
    telegramID=a[2]
    reagent=a[3]
    isAdmin=a[4]
    payed=a[5]
    payedThisMount=a[6]
    regDate=a[7]
    lastPaymentDate=a[8]  
    dbconnect.commit()
    c.close()
    return id,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate,lastPaymentDate

def kickUser(bot, update):

    #print(bot.getChatMember('-1001095318509',175224774))
    try:
        
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        
        a=c.execute("""SELECT regDate,id,isAdmin,payed,payedThisMount,lastPaymentDate,name FROM customer """)
        users = a.fetchall()
        i=0
        print('_______________')
        for user in users:
            print('_______________  '+user[6])
            id=user[1]
            numOfIntroduced=len(c.execute("""SELECT id FROM customer WHERE reagent = ?""",(id,)).fetchall())#tedade kasani ke tavassote in id moarrefi shodeand
            regDate=user[0]
            name=user[6]
            yy=int(regDate[0:4])
            mm=int(regDate[5:7])
            dd=int(regDate[8:10])
            allUsingDays=(date.today()- date(yy,mm,dd)).days


            lastPaymentDate=user[5]
            lastPaymentYear=int(lastPaymentDate[0:4])
            lastPaymentMount=int(lastPaymentDate[5:7])
            lastPaymentDay=int(lastPaymentDate[8:10])
            payedUsingDays=(date.today()- date(lastPaymentYear,lastPaymentMount,lastPaymentDay)).days


            isAdmin=user[2]
            payed=user[3]
            payedThisMount=user[4]
            lastPaymentDate=user[5]
            
            token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
            method='sendMessage'
            
            for channel in channelAddress:
                
                response = requests.post(
                        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                        data={'chat_id': '@testchannel12365478954', 'text':str(id)+' '+str(channel)+' '+bot.getChatMember(channel,id)["status"]+'  '}
                        ).json()
                
            
            if (bot.getChatMember('@testchannel12365478954','114594756')["status"] == 'member'):
                chatTitle=bot.getChat('-1001052560807')["title"]
                if (payed==0):
                    if(allUsingDays>7): #adn also dosn't have any payment
                        txt1=name + ' عزيز\n'+'مهلت استفاده رايگان شما از کانال ' +   chatTitle  +'  به پايان رسيده است، براي خريد اشتراک به @onlineFileAdmin پيام بدهيد.'
                        print(txt1)
                        response = requests.post(
                        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                        data={'chat_id': '@testchannel12365478954', 'text':txt1+' 111 '}
                        ).json()
                        #kickuser()
                    elif(allUsingDays > 1 and numOfIntroduced<5):
                        txt1=name +' عزيز\n '+' مهلت استفاده رايگان شما از کانال ' +   chatTitle +'  به پايان رسيده است، براي خريد اشتراک به @onlineFileAdmin پيام بدهيد. \n'
                        txt2='\n پيشنهاد ويژه براي شما:\n شما ميتوانيد با عضو کردن 5 نفر ديگر در اين ربات، باز هم بصورت رايگان از کانالهاي بات استفاده کنيد. '
                        print(txt1+txt2)
                        response = requests.post(
                        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                        data={'chat_id': '@testchannel12365478954', 'text':txt1+txt2+' 222 '}
                        ).json()
                        #send Msg and kickUser()
                    
                elif (payed==1):
                    if(payedUsingDays> 30):
                        txt1=update.message.from_user.first_name + ' '+update.message.from_user.last_name +'عزيز\n'
                        txt2=' اشتراک شما براي استفاده از کانال '+ chatTitle +'  تمام شده است، براي خريد اشتراک با @onlineFileAdmin در تماس باشيد. '
                        #print(allUsingDays)
                        response = requests.post(
                        url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                        data={'chat_id': '114594756', 'text':txt1+txt2}
                        ).json()
                        
                        #kickuser()
                
            #print(str(response) )
            
                #if (payed==1):
                    #if(payedUsingDays> 30):
                     #   send Msg and kickUser
                     # 
                #elif (payed != 1):
                    #if(allUsingDays>1 and numOfIntroduced < 5):
                     #txt1='مهلت استفاده رايگان شما به پايان رسيده است، براي خريد اشتراک به @onlineFileAdmin پيام بدهيد.'
                     #txt2='پيشنهاد ويژه براي شما:\n شما ميتوانيد با عضو کردن 5 نفر ديگر در اين ربات، باز هم بصورت رايگان از کانالهاي بات استفاده کنيد.'
                     #send Msg and kickUser()
                    #if(allUsingDays>7):
                         #txt1='مهلت استفاده رايگان شما به پايان رسيده است، براي خريد اشتراک به @onlineFileAdmin پيام بدهيد.'
                        #send Msg and kickUser
                     
        dbconnect.commit()
        c.close()
        
    
        #bot.kickChatMember('-1001095318509','114594756')
    except Exception as e:
        print(str(e))
def isAdmin(bot, update):
    
    try:
        db="soverflow.sqlite"
        #print('here3')
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        #print('here2')
        a=c.execute("""SELECT isAdmin
                              FROM customer
                              WHERE id=?""",(update.message.from_user.id,))
        user = a.fetchone()
        dbconnect.commit()
        c.close()
        if(user[0]==0):
            return False
        elif(user[0]==1):
            return True
        
    except Exception as e:
      update.message.reply_text('خطا در برقراري ارتباط... لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد.')


def pay(bot, update):#sabte afradi ka Pardakht dashtehand    
    try:
        if(isAdmin(bot, update)):
        
            if(update.message.text[0:4]=='/pay' and update.message.text[5:7]=='id' ):
                  
                if(update.message.text[8:].isdigit() and existUser(int(update.message.text[8:]))):
                   #HERE: Admin send a message like ('/pay id xxxx')
                    print('aaa')
                    try:                            
                       db="soverflow.sqlite"
                       dbconnect = sqlite3.connect(db)
                       c = dbconnect.cursor()
                       todayDate=str(date.today())
                       print(todayDate)
                       #a=c.execute("UPDATE customer SET (payed,lastPaymentDate)=( '1' , " +todayDate+ " ) WHERE id=?",(int(update.message.text[8:])),)
                       a=c.execute("""UPDATE customer SET  payed=1,payedThisMount=1,lastPaymentDate='""" +str(date.today())+"""' WHERE id=?""",(update.message.text[8:],))
                       if(c.rowcount):
                           update.message.reply_text('عمليات با موفقيت انجام شد.')
                       else:
                           update.message.reply_text('در عمليات بروز رساني مشکلي پيش آمده لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
                       dbconnect.commit()
                       c.close()
                    except Exception as e:
                        update.message.reply_text('در ارتباط با پايگاه داده مشکلي بوجود آمده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
                        print('::: '+str(e))
                else:# HERE: if import id isn't Int or id not exist
                    update.message.reply_text('لطفا آي دي را به درستي وارد کنيد.\n'+str(update.message.text[8:] + ' موجود نميباشد.'+'\n.'))
        else:
                update.message.reply_text(update.message.text)
    except Exception as e:
        update.message.reply_text('در اجرای عملیات مشکلي بوجود آمده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
        print(str(e))


        
token='418884169:AAHkhQ7zbTR4Jlc985kZ2pENRHWHm6guax4'
updater = Updater(token)

rowData=open('original_adress_test.txt','r').read().split('#')
splitedData=[]
for line in rowData:
    #split columns of txt file by 
    splitedData.append(line.split(';'))
print(len(splitedData))
channelAddress=[]
for i in range(int(len(splitedData)-1)):#int(len(splitedData)-10)
    channelAddress.append(splitedData[i+1][1])




#_____________________________User side Fuctions_______________________
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('eshterak', eshterak))
updater.dispatcher.add_handler(CommandHandler('ozv', ozv))
updater.dispatcher.add_handler(CommandHandler('commands', commands))
updater.dispatcher.add_handler(CommandHandler('activeusers', activeUsers))
updater.dispatcher.add_handler(CommandHandler('showId', showId))


updater.dispatcher.add_handler(CallbackQueryHandler(button))
#_______________________________________________________________________
#_______________________________________________________________________




#_____________________________Admin side Fuctions_______________________
updater.dispatcher.add_handler(CommandHandler('pay', pay))
updater.dispatcher.add_handler(MessageHandler(Filters.text, pay))
updater.dispatcher.add_handler(CommandHandler('kickuser', kickUser))
updater.dispatcher.add_handler(CommandHandler('hi', hi))




#_______________________________________________________________________
updater.start_polling()
updater.idle()









