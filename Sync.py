import sqlite3
import requests
import datetime

def sync():
    ns=0
    s1=0
    flag=0
    delr=0
    conn=sqlite3.connect('att.db')
    c=conn.cursor()
    #c.execute('''drop table attendance''')
    #c.execute('''drop table logs''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs(synced varchar,notsynced varchar,deleted varchar,sync_time varchar)''')
    c.execute('''SELECT * FROM settings''')
    s=c.fetchone()
    api=str(s[2])+'api_attendance/att_in'
    apio=str(s[2])+'api_attendance/att_out'
##    c.execute('''select * from attendance''')
##    i=c.fetchone()
##    t={'std_id':i[1],'date':i[2],'time_in':i[3],'key':s[0],'token':s[1]}
##    print(t)
##    response = requests.post(url=api,data=t)
##    print(response.content)
    #print(apio)
    c.execute('''select * from attendance where status=0''')
    for i in c.fetchall():
        #print(o)
        #print(t)
        if i[4]:
            o={'std_id':i[1],'duration':i[5],'time_out':i[4],'key':s[0],'token':s[1],'date':i[2]}
            #print(o)
            #print("Exit time block")
            flag=1
            se = requests.session()
            response = se.post(url=apio,data=o)
            if response.content==b'1':
                #print("Status bit changed")
                #c.execute('''UPDATE attendance SET status=? WHERE std_id=?''',('1',i[1]))
                #conn.commit()
                s1=s1+1
                print('Record Deleted as Synced(Leave time present)')
                c.execute('''DELETE FROM attendance WHERE std_id=?''',(i[1],))
                delr=delr+1
                conn.commit()
            elif response.content==b'0':
                ns=ns+1
            else:
                print(response.content)
        elif i[6]=='0':
            #print("status 0 block")
            t={'std_id':i[1],'date':i[2],'time_in':i[3],'key':s[0],'token':s[1]}
            #print(t)
            se = requests.session()
            response = se.post(url=api,data=t)
            #print(response.content)
            flag=1
            if response.content==b'1':
                print("Status bit changed")
                c.execute('''UPDATE attendance SET status=? WHERE std_id=?''',('1',i[1]))
                conn.commit()
                s1=s1+1
            elif response.content==b'Invaid Admission ID..':
                print("Invalid Admission ID so record deleted")
                c.execute('''DELETE FROM attendance WHERE std_id=?''',(i[1],))
                conn.commit()
            elif response.content==b'0':
                ns=ns+1
            else:
                print(response.content)
    if flag==1:
        now = datetime.datetime.now()
        time=now.strftime("%H:%M:%S")
        c.execute('''INSERT INTO logs values(?,?,?,?)''',(str(s1),str(ns),str(delr),time))
        conn.commit()
        c.execute('''SELECT * FROM logs''')
        print(c.fetchall())
    conn.close()  
sync()
