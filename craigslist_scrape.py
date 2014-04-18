# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from bs4 import BeautifulSoup
import requests
import re

# <codecell>

class Post(object):
    def __init__(self, url, price=None):
        self.url = url
        self.price = price
        self.postsoup = None
        
    @classmethod
    def find_price(cls, post):
        results = post.find('span', attrs={'class':'price'})
        if results is None: 
            return results
        return results.contents[0].replace('$','')
    
    def parse_post_metadata(self):
        # Only do if soup doesn't already exist.
        if self.postsoup is None:
            self.get_post_soup()
        self.title = self.postsoup.title.text
        self.anon_email = self.get_anon_email()
        self.user_email = self.get_user_email()
        self.posted_time = self.get_posted_time()
        self.updated_time = self.get_updated_time()
        self.postid = re.search('/(\d+).htm', self.url).groups()[0]
        self.text = self.postsoup.find('section', id='postingbody').text.strip()
        
    def get_post_soup(self):
        """Load the soup for the page of the posting if not already loaded.
        """
        r = requests.get(self.url)
        self.postsoup = BeautifulSoup(r.text) 
    
    def get_anon_email(self):
        """Grab the anonomized email address from the link provided on the posting page"""
        try:
            return parse_anonemail(self.postsoup)
        except:
            return None
        
    def get_user_email(self):
        """Grab any emails the poster provided in the text of the page"""
        try:
            return parse_useremail(self.postsoup) 
        except:
            return None
        
    def get_posted_time(self):
        try:
            for pclass in self.postsoup.find_all('p', class_='postinginfo'):
                if 'Posted:' in pclass.text:
                    return pclass.time['datetime']
            return None
        except:
            return None
            
    def get_updated_time(self):
        try:
            for pclass in self.postsoup.find_all('p', class_='postinginfo'):
                if 'updated:' in pclass.text:
                    return pclass.time['datetime']
            return None
        except:
            return None
        
def parse_anonemail(soup):
    for link in soup.find_all('a'):
        match = re.search('([a-zA-Z0-9._%+-]+@\w+\.craigslist\.[\w]{2,4})', link.get('href'))
        if match is not None:
            return match.group(1)
    return None

def parse_useremail(soup):
    re.search('([a-zA-Z0-9._%+-]+@[a-zA-z0-9.-]+\.[\w]{2,4})', soup.get_text())   
    
def get_city(soup):
    """Using the breadcrumbs at the top of all craigslist pages, figure out what city you're in.
    """
    return soup.find_all('span', class_='crumb')[1].a.text

# <codecell>

class Search(object):
    def __init__(self, ccity, ccategory, query=None, csearchtype='A', chood=None, minask=None, maxask=None, haspic=False):
        self.ccity = ccity
        self.ccategory = ccategory
        self.query = query
        self.csearchtype = csearchtype #possibilities: A=all, T=title
        self.chood = chood
        self.minask = minask
        self.maxask = maxask
        self.haspic = haspic
        
        self.cminask = '' if minask is None else str(minask)
        self.cmaxask = '' if maxask is None else str(maxask)
        self.chaspic = '1' if haspic else '0'
        
    def format_search_url(self):
        #http://seattle.craigslist.org/search/sya/est?query=lenovo&zoomToPosting=&srchType=T&minAsk=10&maxAsk=10000&hasPic=1
        if self.query == None:
            return 'http://{0}.craigslist.org/{1}{2}'.format(self.ccity, postslash(self.chood), self.ccategory)
        return 'http://{0}.craigslist.org/search/{1}{7}?query={2}&srchType={3}&minAsk={4}&maxAsk={5}&hasPic={6}'.format(
                    self.ccity, self.ccategory, self.query, self.csearchtype, self.cminask, self.cmaxask, 
                    self.chaspic, preslash(self.chood))
    
    def find_postings(self):
        pass
    
        
postslash = lambda x: '' if x is None else x+'/'
preslash = lambda x: '' if x is None else '/'+x

# <codecell>

ms = Search('seattle', 'mcy', query='sport', chood='see', csearchtype='A', minask=1, maxask='10000')
site = ms.format_search_url()
print site
r = requests.get(site)
soup = BeautifulSoup(r.text)   

# <codecell>

url = "http://seattle.craigslist.org/search/fua/see?zoomToPosting=&catAbb=fua&query=bed+frame&minAsk=&maxAsk=&excats="
re.search('.craigslist.org

# <codecell>

postings = soup('p')

for bs4tag in postings[:10]:  
    post_href = bs4tag('a')[1].get('href')[1:]
    post = Post('http://%s.craigslist.org/'%ms.ccity + post_href, Post.find_price(bs4tag))
    post.parse_post_metadata()
    print post.title
    print '$', post.price
    print post.posted_time
    print post.updated_time
    print post.postid
    print post.user_email
    print post.url
    print

# <headingcell level=1>

# Scratch

