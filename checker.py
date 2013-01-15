# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 15:01:51 2013

@author: gallamine
"""
import email, getpass, imaplib, csv, sys

detach_dir = '.' # directory where to save attachments (default: current)
#user = raw_input("Enter your GMail username:")

user = str(sys.argv[1])        # YOUR GMAIL ACCOUNT
pwd = str(sys.argv[2])          # GMAIL PASSWORD
sendTo = str(sys.argv[3])       # YOURPHONENUMBER@vzwpix.com



# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)
m.select("inbox")
#m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

searchString = '(UNSEEN) (FROM "' + sendTo + '")'
resp, items = m.search(None,searchString)
print resp
#mset = imap.Search("UNSEEN",fetchUIds);
#OR (SUBJECT \"SSL\") (SUBJECT \"Python\")
items = items[0].split() # getting the mails id

with open('taskData.csv', 'ab') as csvfile:
    dataCSV = csv.writer(csvfile)
    #dataCSV.writerow(['time','task'])
    # These are all the unseen status updates
    for emailid in items:
        print "Getting messages"
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc

        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
        
        if mail.get_content_maintype() != 'multipart':
            continue
        
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue
    
            # is this part an attachment ?
            if part.get('Content-Disposition') is None:
                continue
    
            filename = part.get_filename()
            counter = 1
    
            # if there is no filename, we create one with a counter to avoid duplicates
            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1
    
            task = part.get_payload(decode=True)
            print task
            dataCSV.writerow([mail['Date'],task])