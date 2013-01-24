# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:52:20 2013

@author: gallamine
"""
# http://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
#import email, getpass, imaplib, os
#
#detach_dir = '.' # directory where to save attachments (default: current)
#user = raw_input("Enter your GMail username:")
#pwd = getpass.getpass("Enter your password: ")

import smtplib,csv, datetime,random,time, sys
from time import gmtime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

gmail_user = str(sys.argv[1])       #"YOURGMAILACCOUNT@gmail.com"
gmail_pwd = str(sys.argv[2])        
sendTo = str(sys.argv[3])           # "YOURVERIZONNUMBER@vtext.com"
sendRate = 30.0                      # Average sending rate in minutes

def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

#   part = MIMEBase('application', 'octet-stream')
#   part.set_payload(open(attach, 'rb').read())
#   Encoders.encode_base64(part)
#   part.add_header('Content-Disposition',
#           'attachment; filename="%s"' % os.path.basename(attach))
#   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

with open('/Users/gallamine/Documents/PythonStuff/SMSTimeChecker/taskData.csv', 'rwb') as csvfile:
    print "Checking time"
    dataCSV = csv.reader(csvfile)
    for row in dataCSV:
        lastRxTime = row[0]
    lastTime = datetime.datetime.strptime(lastRxTime, "%a, %d %b %Y %H:%M:%S +0000")
    # This logic is crap. We need to figure out if the last ping has been logged before sending another one ... 
    if lastTime < datetime.datetime.utcnow():
        if random.random() < (1/sendRate):
            print "Sending mail"
            #outCSV = csv.writer(csvfile)
            #outCSV.writerow([time.strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),''])
            mail(sendTo,"","What'r you working on?","")
   