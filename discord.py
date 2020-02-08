import requests
import json
from time import sleep

loginrequst = requests.Session()

def deleteMessages(ids):
    print("\nDeleting Messages...")
    for id in ids:
        deleteMessagesRequest = requests.delete(url='https://discordapp.com/api/v6/channels/' + memberid + '/messages/' + id, headers={'Authorization': token})
        sleep(0.5)
    print("\nDone!")
    print("\nDo you want to do it again?\n\nEnter 1 or 2")
    if input("\n1. Yes\n2. No\n\n> ") == "1":
        member = input('\nConversation ID: ')
        messages = int(input('\nMessages to delete: '))
        declareHeaders(email, password, member, messages)
    else:
        pass

def iterateList(pJson):
    messagesIDArray = []
    n = 0

    # Add message ID's that were sent from the main user
    while n < len(pJson):
        if pJson[n]['author']['username'] == user:
            messagesIDArray.append(pJson[n]['id'])
        n+=1
    deleteMessages(messagesIDArray)

def loginRequest(headers, postdata, id, limit):
    global token
    print("\nLogging in...")
    # Main Login Request
    loginrequest = requests.post(url="https://discordapp.com/api/v6/auth/login", data=postdata, headers=headers)

    # Gets the token from the Login request's response
    token = loginrequest.text.split('"')[3]

    print("\nParsing Messages...")
    
    # Makes a request to receive list of messages with desired amount of messages displayed
    messagesRequest = requests.get(url="https://discordapp.com/api/v6/channels/%s/messages?limit=%d" % (id, limit*2) , headers={'Authorization': token})
    parsed_json = json.loads(messagesRequest.text)
    iterateList(parsed_json)

def declareHeaders(usr, pw, convid, msgamount):
    loginheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://discordapp.com"}

    logindata = '{"email":"%s","password":"%s","undelete":false,"captcha_key":null,"login_source":null,"gift_code_sku_id":null}' % (usr, pw)
    loginRequest(loginheaders, logindata, memberid, msgamount)

if __name__ == '__main__':
    email = input('Email: ')
    password = input('\nPassword: ')
    user = input('\nUsername: ')
    memberid = input('\nConversation ID: ')
    messagesTodelete = int(input('\nMessages to delete: '))

    declareHeaders(email, password, memberid, messagesTodelete)
