# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# 1. Stuff

# <codecell>

from imaplib import IMAP4_SSL
from datetime import date,timedelta,datetime
from time import mktime
from email.utils import parsedate, parsedate_tz
import email
from pylab import plot_date,show,xticks,date2num
from pylab import figure,hist,num2date
from matplotlib.dates import DateFormatter

# <codecell>

class GmailAccount(IMAP4_SSL):
    def __init__(self, username=None, password=None, folder=None):
        self.username = username
        self.password = password
        self.folder = folder
        
    def login(self):
        self.conn = IMAP4_SSL('imap.gmail.com')
        response = self.conn.login(self.username, self.password)
        return response
    
    def search(self, folder, query, readonly=False):
        self.conn.select(folder, readonly)
        resp, data = self.conn.uid('search', None, query)
        return data
    
    def fetch(self, ids, query):
        resp, data = self.conn.uid('fetch', ids[0].replace(' ',','), query)
        return data

# <codecell>

tyler = GmailAccount(username='tyleha@gmail.com',password='56741Tlh')
out = tyler.login()

# <codecell>

interval = (date.today() - timedelta(2)).strftime("%d-%b-%Y")
ids = tyler.search("inbox", '(SENTSINCE {date})'.format(date=interval), True)

# <codecell>

body = '(BODY.PEEK[TEXT])'
headers = '(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE TO CC)])'
data = tyler.fetch(ids, headers)

# <codecell>

from email.parser import HeaderParser
parser = HeaderParser()
msg = parser.parsestr(data[0][1])
print type(msg)

# <codecell>

msg.keys()

# <codecell>

import pandas as pd

# <codecell>

df = pd.DataFrame({'a': [0, 3], 'b': [1, 4], 'c': [2, 5]})
df = pd.concat((pd.DataFrame({'a': [10], 'b': [10], 'c': [10]}), df))
print df
for row, stuff in df.iteritems():
    print row
    print stuff
#df = df*-1
#xx = df.cumsum()
#xx.fillna(0)
#xx =xx- 10
#df

df.map()

# <codecell>

df.diff()

# <codecell>

df.diff(-1)

# <codecell>

Sample DataFrame 
     a   b   c
1    10  10  10
0    0   1   2
1    3   4   5


New DataFrame created
     a     b    c
0    -10   -9   -8
1    -13    5    3

