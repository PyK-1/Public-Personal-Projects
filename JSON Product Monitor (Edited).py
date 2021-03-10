import bs4
import requests
import smtplib
import time
import json
from datetime import date
from email.message import EmailMessage


getPageJson = requests.get('https://yourwebsite.com/products.json')

products = json.loads((getPageJson.text))['products']

productList = []
dateToday = str(date.today())

for i in products:
    if "Keyword" in i['title'] or "Keyword" in i['title'] or "Keyword" in i['title'] or "Limited" in i['title']:
        itemPublishDate = (i['published_at'])
        itemUpdateDate = (i['updated_at'])
        if dateToday in itemUpdateDate or dateToday in itemPublishDate:
            productList.append(i['title'])
            productList.append("Most Recent Publish Time: " + i['published_at'])
            productList.append("Most Recent Update Time: " + i['updated_at'])
            productList.append("\n")


productListCount = len(productList)/4 # Divided by the 4 values of each value of the list

productChange = False

# While loop for the stock baseline; exits program after 2 seconds
while productListCount == 0:
    print("No changes to products...")
    print("Today's Product List Count:",productListCount)
    print("-"*40)
    for i in productList:
        print(i)
    time.sleep(2)
    exit()

# E-mail list
toAddress = ['abc@gmail.com','xyz@gmail.com']


# If statement that prints the new productListCount when there's a change
if productListCount != 0:
    productChange = True
    print("---"*10+"THERE WAS A CHANGE IN PRODUCTS!!!"+"---"*10)
    print("Today's Product List Count:",productListCount)
    print("-"*40)
# Product Names listed if there's a change
    for x in productList:
        print(x)


if productChange:
    msg = EmailMessage()
    host = "smtp.gmail.com"
    port = 587
    email_username = 'youremailbot@gmail.com'
    email_password = 'youremailbotpassword'
    to_list = toAddress

    msg['From'] = email_username
    msg['Subject'] = 'PRODUCTS HAVE CHANGED!!!'
    msg['To'] = to_list #you can loop through a list of emails to send this mail to everyone on the list

# New products alerted to have been added to the body of the email with most recent publish/update times
    msg.set_content('plain text email')
    msg.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <p>{'<br/>'.join(productList)}</p>
            </body>
        </html>
        """, subtype='html')

    with smtplib.SMTP(host, port) as smtp:
        smtp.starttls()
        smtp.login(email_username, email_password)
        smtp.send_message(msg)
        print("Sent notification email for:",toAddress)
        time.sleep(2)
        exit()
