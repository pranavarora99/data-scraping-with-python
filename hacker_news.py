import requests
from bs4 import BeautifulSoup

#send email
import smtplib

#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime

now = datetime.datetime.now()

content = ''

#extraction hacker news story
def extract_news(url):
    print('extracting hacker news stories....')
    cnt = ''
    cnt += ('<b>HACKER NEWS top stories</b>\n' + '<br>' + '-' *50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title','valign':''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-----------------------<br>')
content += ('<br><br>Have a good day.')

#sending email
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = 'pranavarora99.pa@gmail.com'
TO = 'pranavarora99.pa@gmail.com'
PASS = '***********'

msg = MIMEMultipart()

#msg.add_header('content-disposition', 'attatchment', filename='empty.txt')
msg['Subject'] = 'Top storied from Hacker News [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)

msg.attach(MIMEText(content, 'html'))

print('Starting Server')

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Successfully Sent')

server.quit()