# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup
import requests
import re

# <codecell>

class Post(object):
    def __init__(self, bs4tag, rooturl):
        self.href = bs4tag('a')[1].get('href')[1:]
        self.title = bs4tag('a')[1].text 
        self.rooturl = rooturl
        self.url = self.rooturl + self.href
        self.price = Post.find_price(bs4tag)
        
        self.postsoup = None
        
    @classmethod
    def find_price(cls, post):
        results = post.find('span', attrs={'class':'price'})
        if results is None: 
            return results
        return results.contents[0].replace('$','')
    
    def get_post_soup(self):
        # Only do if soup doesn't already exist.
        if self.postsoup is None:
            r = requests.get(self.url)
            self.postsoup = BeautifulSoup(r.text) 
    
    def get_anon_email(self):
        """Grab the anonomized email address from the link provided on the posting page"""
        self.get_post_soup()
        self.anonemail = parse_anonemail(self.postsoup)
        return self.anonemail
        
    def get_user_email(self):
        """Grab any emails the poster provided in the text of the page"""
        self.get_post_soup()
        self.useremail = parse_useremail(self.postsoup) 
        return self.useremail
        
def parse_anonemail(soup):
    for link in soup.find_all('a'):
        match = re.search('([a-zA-Z0-9._%+-]+@\w+\.craigslist\.[\w]{2,4})', link.get('href'))
        if match is not None:
            return match.group(1)
    return None

def parse_useremail(soup):
    re.search('([a-zA-Z0-9._%+-]+@[a-zA-z0-9.-]+\.[\w]{2,4})', soup.get_text())   
    

# <codecell>

class Search(object):
    def __init__(self, ccity, ccategory, query=None, csearchtype='A', chood=None, minask=None, maxask=None, haspic=False):
        self.ccity = ccity
        self.ccategory = ccategory
        self.query = query
        self.csearchtype = csearchtype
        self.chood = chood
        self.minask = minask
        self.maxask = maxask
        self.haspic = haspic
        
        self.cminask = '' if minask is None else str(minask)
        self.cmaxask = '' if maxask is None else str(maxask)
        self.chaspic = '1' if haspic else '0'
        
    def search_url(self):
        #http://seattle.craigslist.org/search/sya/est?query=lenovo&zoomToPosting=&srchType=T&minAsk=10&maxAsk=10000&hasPic=1
        if self.query == None:
            return 'http://{0}.craigslist.org/{1}{2}'.format(self.ccity, postslash(self.chood), self.ccategory)
        return 'http://{0}.craigslist.org/search/{1}{7}?query={2}&srchType={3}&minAsk={4}&maxAsk={5}%hasPic={6}'.format(
                    self.ccity, self.ccategory, self.query, self.csearchtype, self.cminask, self.cmaxask, self.chaspic, preslash(self.chood))
    
    def find_postings(self):
        pass
    
        
postslash = lambda x: '' if x is None else x+'/'
preslash = lambda x: '' if x is None else '/'+x

# <codecell>

ms = Search('seattle', 'ppa', query='pink', chood='see', csearchtype='A', minask=1, maxask='1000')
site = ms.search_url()
r = requests.get(site)
soup = BeautifulSoup(r.text)   

# <codecell>

postings = soup('p')

for bs4tag in postings[:10]:  
    post = Post(bs4tag, rooturl)
    print post.title
    print post.url
    print post.price
    print post.get_anon_email()
    print post.get_user_email()
    print

# <codecell>


# <codecell>


