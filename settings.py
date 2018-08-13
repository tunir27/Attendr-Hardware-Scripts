import sqlite3
import json
import requests

def setting():
    connl=sqlite3.connect('att.db')
    cl=connl.cursor()
    print("Enter Key")
    key=input()
    print("Enter URL")
    url=input()
    response = requests.post("https://app.schoolbios.com/index.php/login/verify_app",data={'key':key,'website':url})
    data = response.json()
    #print(response.status_code)
##    if data['type']==0:
##       print("Authenticated token:"+ data['token'])
##    else:
##        print("Failed "+ data['error'])
    cl.execute('''CREATE TABLE IF NOT EXISTS settings(key varchar2 PRIMARY KEY,token varchar2,url varchar2)''')
    cl.execute('''INSERT INTO settings values(?,?,?)''',(key,data['token'],url))
    connl.commit()
    cl.execute('''SELECT * FROM settings''')
    print(cl.fetchall())
    connl.close()
setting()
