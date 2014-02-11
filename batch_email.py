# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

rcps = []

with open(r'C:\Users\Tyler\Documents\My Dropbox\Wedding\Wedding Guest List.csv') as csvfile:
#with open(r'C:\Users\Tyler\Documents\My Dropbox\Wedding\test.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        #print row
        names = row[0].strip().split(',')
        addrs = row[7].strip().split(' ')
        
        #print addrs
        if addrs == ['']: continue
        
        for i, addr in enumerate(addrs):
            rcps.append((addr.strip(), names[i].strip()))


for email in rcps:
    try:
        me = "Tyler and Jen"
        you = email[0]
        name = email[1].split(' ')[0] #the first word in name
        rsp = 'n'
        while rsp != 'y':
            rsp = raw_input('About to email to %s with first name %s. Proceed? '%(you, name))
            if rsp.lower() == 'y': pass
            elif rsp.lower() == 'n': 
                raise TypeError, 'Something wrong with the address or name'
                    

        print "Emailing..."
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Save the Date"
        msg['From'] = me
        msg['To'] = you
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.ehlo()
        server.login('tyleha', '56741Tlh')
        
        # Create the body of the message (a plain-text and an HTML version).
        text = "Hey %s, \n\nWe're getting married on November 9, 2013 in Charlottesville, Virginia -- Save the Date! We hope we see you there.\n\ntyandjen.weebly.com\n\nTyler and Jen"%name
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hey %s,<br><br>
               We're getting married on November 9, 2013 in Charlottesville, Virginia -- <a href="http://www.tyandjen.weebly.com">Save the Date!</a> We hope we see you there.<br><br>
               Tyler and Jen
            </p>
          </body>
        </html>
        """%name
        
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        # Attach parts into message container.
        msg.attach(part1)
        msg.attach(part2)
        
        out = server.sendmail(me, you, msg.as_string())
        if out == {}:
            print "Successfully emailed"

        server.close()
    except Exception as e:
        print e
        f = open('errors.txt', 'a')
        f.write(you+'\n')
        f.close()



