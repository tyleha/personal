# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
import boto
from fetch.aws import aws_ak, aws_sk

# <codecell>

conn = boto.connect_ses(aws_ak, aws_sk)
conn.send_email('python@tylerhartley.com', "test subject", "the test body!!\nAnd stuff", to_addresses=['python@tylerhartley.com'])

# <codecell>

import smtplib
import string
 
SUBJECT = "Test email from Python"
TO = "tyleha@gmail.com"
FROM = "python@tylerhartley.com"
text = "blah blah blah"
BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
        ), "\r\n")
server = smtplib.SMTP("mail.tylerhartley.com")
server.sendmail(FROM, [TO], BODY)
server.quit()

# <codecell>


