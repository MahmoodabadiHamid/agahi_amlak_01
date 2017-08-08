try:
    import sqlite3
except:
    from pysqlite2 import dbapi2 as sqlite3

#prepare testcase
user_ID=2252254
db="bsoverflow.sqlite"
dbconnect = sqlite3.connect(db)
c = dbconnect.cursor()

#c.execute("""CREATE TABLE IF NOT EXISTS customer
 #                   (id int not null primary key, name varchar(50), telegramID varchar(30),reagent int(20) not null DEFAULT 175224774,isAdmin bool not null DEFAULT 0,
  #                  `payed` INTEGER DEFAULT 0)""")
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID,'bb0ham mah','@bbaaa','255','0','100'))
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID+1,'bb0ham mah','@WERWERaa','255','0','100'))
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID+2,'bb0ham mah','@bXXCVbaaa','255','0','100'))
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID+3,'bb0ham mah','@bbaaa','255','0','100'))
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID+4,'bb0ham mah','@;kp','255','0','100'))
c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed) VALUES (?,?,?,?,?,?)""",(user_ID+5,'bb0ham mah','@adwe','255','0','100'))

a=c.execute("""SELECT telegramID
                          FROM customer
                          WHERE reagent=?""",(int(255),))
rows = a.fetchall()
i=0
for row in rows:
        i+=1
        print(row)
print(i)
