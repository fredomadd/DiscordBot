import requests
import json
from time import sleep

loginrequest = requests.Session()

def deleteMessages(ids):
    n = 0
    for id in ids:
        n+=1
        print("Deleting Messages (" + str(n) + "/" + str(len(ids)) + ")")
        delreqs = requests.delete(url='https://discordapp.com/api/v6/channels/' + userid + '/messages/' + id, headers={'Authorization': token})
    print("Done!")
    print("\nDo you want to do it again?\nEnter 1 or 2")
    if input("\n1. Yes\n2. No\n\n> ") == "1":
        beginning()
    else:
        pass

def parseMessages(msgamount):
    print("Parsing Messages...")
    global ids, messages, friendids, friendmessages
    ids = []
    messages = []
    friendids = []
    friendmessages = []

    firstHundred = requests.get(url="https://discordapp.com/api/v6/channels/" + userid + "/messages?limit=100", headers={'Authorization': token})
    index = json.loads(firstHundred.text)[-1]['id']

    # Add the ID's of the first hundred
    for fids in json.loads(firstHundred.text):
        if fids['author']['username'] == ownuser and len(ids) <= msgamount:
            ids.append(fids['id'])
            messages.append(fids['content'])

    # Whole thing is to parse all the messages using a function that is running recursively
    def parseOldMessages():
        request = requests.get(url="https://discordapp.com/api/v6/channels/" + userid + "/messages?before=" + index + "&limit=100", headers={'Authorization': token})
        lastindex= json.loads(request.text)[-1]['id']
        requestdata = json.loads(request.text)
        return requestdata, lastindex

    try:
        while len(ids) <= msgamount:
            f1 = parseOldMessages()
            data = f1[0]
            index = f1[1]
            for idd in data:
                if idd['author']['username'] == ownuser and len(ids) < msgamount:
                    ids.append(idd['id'])
                    messages.append(idd['content'])
                elif idd['author']['username'].lower() == frienduser:
                    friendids.append(idd['id'])
                    friendmessages.append(idd['content'])
        deleteMessages(ids)
    except IndexError:
        deleteMessages(ids)

def parseUsers(targetuser, msgamount):
    # Parse own username and target's user id
    global userid, ownuser, ownuserid
    print("Parsing usernames...")

    # Getting our username
    reqs = requests.get("https://discordapp.com/api/v6/users/@me", headers={'Authorization': token})

    ownuser = json.loads(reqs.text)['username']
    ownuserid = json.loads(reqs.text)['id']

    # Getting Target's user ID
    reqs = requests.get(url="https://discordapp.com/api/v6/users/@me/channels", headers={'Authorization': token})
    parsed_json = json.loads(reqs.text)

    try:
        n = 0
        while parsed_json[n]['recipients'][0]['username'].lower() != targetuser.lower():
            n = n + 1
        userid = parsed_json[n]['id']
    except IndexError:
        print("User not found")
    parseMessages(msgamount)

def loginrequest():
    global token
    print("\nLogging in...")
    loginheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://discordapp.com"}

    logindata = '{"email":"%s","password":"%s","undelete":false,"captcha_key":null,"login_source":null,"gift_code_sku_id":null}' % (email, password)
    loginrequest = requests.post(url="https://discordapp.com/api/v6/auth/login", data=logindata, headers=loginheaders)

    if 'Password does not match.' in loginrequest.text:
        print("Password is incorrect.")
    elif 'mfa": true' in loginrequest.text:
        print("Can't login through 2FA, sorry.")
    else:
        token = loginrequest.text.split('"')[3]
        parseUsers(frienduser, messagesTodelete)

def beginning():
    global frienduser, messagesTodelete
    frienduser = input('Friend Username (Name only!): ')
    messagesTodelete = int(input('Messages to delete (Type \'0\' if you want to delete all): '))
    if messagesTodelete == 0:
        messagesTodelete = 100000

    loginrequest()

if __name__ == '__main__':
    email = input('Email: ')
    password = input('Password: ')
    beginning()
