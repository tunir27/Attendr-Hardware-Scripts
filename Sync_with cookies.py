import sqlite3
import requests
import datetime
import pickle
import requests
import os
#import subprocess
#os.system("test -e cookies.txt || touch cookies.txt")  #uncomment this
def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
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
            flag=1
            f=os.stat("cookies.txt").st_size == 0
            filename="cookies.txt"
            if f:
                #save cookies
                response= requests.post(url=apio,data=o)
                #print(response.content)
                save_cookies(response.cookies, filename)
            else:
                #load cookies and do a request
                print("OUT Block")
                response=requests.post(url=apio, data=o,cookies=load_cookies(filename))
                #print(response.content)
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
            f=os.stat("cookies.txt").st_size == 0
            filename="cookies.txt"
            if f:
                #save cookies
                response= requests.post(url=api,data=t)
                #print(response.content)
                save_cookies(response.cookies, filename)
            else:
                print("IN Block")
                #load cookies and do a request
                response=requests.post(url=api, data=t,cookies=load_cookies(filename))
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
    #subprocess.call(["truncate", "-s", "0", "cookies.txt"])   #uncomment this
    if flag==1:
        now = datetime.datetime.now()
        time=now.strftime("%H:%M:%S")
        c.execute('''INSERT INTO logs values(?,?,?,?)''',(str(s1),str(ns),str(delr),time))
        conn.commit()
        c.execute('''SELECT * FROM logs''')
        print(c.fetchall())
    conn.close()  
sync()
