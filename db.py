import sqlite3
import datetime
import time
#import Read1
#import sync
#from datetime import datetime
conn = sqlite3.connect('att.db')
c = conn.cursor()

def db(sid):
    #conn = sqlite3.connect('att.db')
    #c = conn.cursor()
    start_time = time.time()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance(ID integer PRIMARY KEY,std_id varchar2,entry_date varchar2,entry_time varchar2,leave_time varchar2,duration varchar2,status varchar2)''')
    #print("Enter the values to be inserted")
    #print("Student ID")
    std_id=sid
    t = (std_id,)
    c.execute('SELECT * FROM attendance where std_id=?',t)
    d=c.fetchone()
    #print(d)
    if d:
        #c.execute('SELECT entry_time FROM attendance where std_id=?',t)
        datetime_object = datetime.datetime.strptime(d[3],'%H:%M:%S')
        dtime=datetime_object.strftime("%H:%M:%S")
        FMT = "%H:%M:%S"
        now = datetime.datetime.now()
        ntime=now.strftime("%H:%M:%S")
        date = datetime.datetime.strptime(str(ntime), FMT) - datetime.datetime.strptime(str(dtime), FMT)
        tdelta = datetime.datetime.strptime(str(date),"%H:%M:%S")
        #h,m,s=tdelta.split(':')
        rtime=int(tdelta.hour)*60+int(tdelta.minute)+(int(tdelta.second)/60)
        #print(rtime)
        #chtime=datetime.datetime.now()-datetime.timedelta(minutes=30)
        if rtime>1:
            exit_att(std_id,d[3])
            #entry_att(std_id)
            #print("Data Inserted")
    else:
        entry_att(std_id)
        #print("Data Inserted")


    #c.execute('''drop table attendance''')
    #entry_att(std_id)
    #printr()
    #sync()
    #conn.close()
    #print(time.time()-start_time)


def entry_att(std_id):
    now = datetime.datetime.now()
    date=now.strftime("%y/%m/%d")
    time=now.strftime("%H:%M:%S")
    c.execute('''INSERT INTO attendance(std_id,entry_date,entry_time,status) values(?,?,?,?)''',(std_id,date,time,'0'))
    conn.commit()


def exit_att(std_id,ptime):
    now = datetime.datetime.now()
    #date=now.strftime("%Y-%m-%d")
    ltime=now.strftime("%H:%M:%S")
    FMT = '%H:%M:%S'
    duration = datetime.datetime.strptime(str(ltime), FMT) - datetime.datetime.strptime(str(ptime), FMT)
    utime=datetime.datetime.strptime(str(duration),"%H:%M:%S")
    dtime=utime.strftime("%H:%M:%S")
    #print(duration,dtime)
    #print(type(duration))
    #print(type(dtime))
    c.execute('''UPDATE attendance SET leave_time=?,duration=?,status=? where std_id=?''',(ltime,dtime,'0',std_id))
    conn.commit()


def printr():
    c.execute('''SELECT * FROM attendance''')
    print(c.fetchall())
