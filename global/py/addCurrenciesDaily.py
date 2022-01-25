import requests
from json import dumps
from time import sleep

LOGIN_NAME = "" # blooket username or email
LOGIN_PASSWORD = "" # password

user_agents = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    'Accept-Encoding': "gzip, deflate",
    'Accept': "application/json",
    'Content-Type': "application/json;charset=utf-8",
    'Accept-Language': "en-GB,en;q=0.9"}
    
# spoofs headers to look like a browser (Safari).
# User agent string obtained from http://www.useragentstring.com/pages/useragentstring.php

session = requests.Session()
session.headers.update(user_agents)

def login(s, name, pw):
    request_url = "https://api.blooket.com/api/users/login"
    request_data = {'name': name, 'password': pw}
    print("(-) Sending login request to Blooket.")
    
    r = s.post(request_url, data=dumps(request_data))
    try:
        r.raise_for_status()
    except:
        print(f"(*) Bad return status code: {r.status_code}")
        quit()
    r = r.json()
    if r["success"]:
        print("(-) Successfully logged in.")
        return True
    else:
        print(f"""(*) Log in unsuccessful.
(*) Error Type: {r['errType']}
(*) Message: {r['msg']}""")
        quit()


def verify_login(s):
    global blooketName
    print("(-) Verifying Blooket session.")
    ver = s.get("https://api.blooket.com/api/users/verify-session")
    try:
        ver.raise_for_status()
    except:
        print(f"(*) Bad return status code: {ver.status_code}")
        quit()
    ver = ver.json()
    if not ver:
        print("(-) Not logged in. Logging in...")
        login(s, LOGIN_NAME, LOGIN_PASSWORD)
        print("(-) Reverifying session.")
        ver = s.get("https://api.blooket.com/api/users/verify-session")
        try:
            ver.raise_for_status()
        except:
            print(f"(*) Bad return status code: {ver.status_code}")
            quit()
        ver = ver.json()
    
    print("(-) Retrieving username.")
    try:
        blooketName = ver["name"]
    except:
        print(f"""(*)  Json object is unexpected.
        If issue persists, open an issue on Github.
{ver}""")
        quit()
    
    print(f"(-) Name set to {blooketName}")
    
    print("(-) Session is verified.")
    return True

    
def addCurrencies(s):
    print("(-) Starting new script cycle...")
    verify_login(s)
    
    request_url = "https://api.blooket.com/api/users/add-rewards"
    request_data = dumps({
        "name": blooketName,
        "addedTokens": 500,
        "addedXp": 300
    })
    print(f"(-) Sending {blooketName} 300 XP and 500 Tokens...")
    r = s.put(request_url, data=request_data)
    
    try:
        r.raise_for_status()
    except:
        print(f"(*) Bad return status code: {r.status_code}")
        
        
        quit()
    print(f"(-) Successfully sent {blooketName} 300 XP and 500 Tokens.")
    return

while True:
    addCurrencies(session)
    print("(-) Sleeping for 24h...")
    sleep(86400)