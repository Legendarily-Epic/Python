from bs4 import BeautifulSoup
import requests
import smtplib
import time

URL = 'https://www.amazon.com/*' #Place web address for item here
headers = {"User Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'} # I used Firefox

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find(id="productTitle").get_text()
price = soup.find(id="priceblock_ourprice").get_text()
converted_price = float(price[1:6])
expected_price = 58.00 #Place whatever your expected price is here

def check_price():

    #Debug helpers
    #print(title.strip())
    #print(converted_price)
    #print(price.strip())

    if(converted_price < expected_price):
        send_mail()

# I used Gmail to send email
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('user@gmail.com','Password') #enter your credentials here
    subject = 'Price has fallen!'
    body = 'The ' + title.strip() + ' has fallen below your expected price of $' + str(expected_price) + ' and is now ' + price + '.'
    body1 = 'Here is the link to go purchase ' + URL
    msg = f"Subject: {subject}\n\n{body}\n\n{body1}"
    #Choose who you want to send the email to? You can send it to the same email you are sending from and can send to multiple
    server.sendmail(
        'user@gmail.com',
        'user@yahoo.com',
        msg
    )
    #Debug helper
    #print('Hey, email has been sent')
    server.quit()

# Loop for frequency you want to check price. I chose once a day
while(True):
    check_price()
    time.sleep(60*60*24)
