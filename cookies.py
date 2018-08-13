import pickle
import requests
import os
def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

#save cookies
def p():
    f=os.stat("cookies.txt").st_size == 0
    filename="cookies.txt"
    if f:
        r = requests.post('https://www.bhoracademy.com/api_auth')
        #print(r.content)
        save_cookies(r.cookies, filename)
        return r.content
    else:
        #load cookies and do a request
        r=requests.post('https://www.bhoracademy.com/api_auth', cookies=load_cookies(filename))
        return r.content
if __name__ == "__main__":
    d=p()
    print(d)
