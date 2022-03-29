from cmath import phase
from http import server
import json
import smtplib
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage

log = ""

def check_availability(url, phrase):
    global log
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features='html.parser')

        if phrase in soup.text:
            return False
        return True
    except:
        log += "ERROR parsing website"



def main():
    url = "https://enter-website-here.com " # enter the store website URL here 
    phrase = "Enter your email address to be notified when this item is back in stock"
    available = check_availability(url, phrase)

    if available:
        
        with open('config.json') as file:
            config = json.load(file)
            #enter credentials in config.json
            username = config['username'] 
            password = config['password']
            fromAddress = config['fromAddress']
            toAddress = config['toAddress']
        msg = EmailMessage()
        #replace <YOUR-ITEM> with the product you're checking eg. PS5
        msg['Subject'] = "<YOUR-ITEM> in Stock!"
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg.set_content("looks like <YOUR-ITEM> is in stock" + url)
        #replace ('smtp.gmail.com', 587) if required 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)

        server.send_message(msg)
        server.quit()
    

if __name__ == '__main__':
    main()