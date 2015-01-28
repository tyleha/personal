# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import instagram as ig
import numpy as np
# import matplotlib.pyplot as plt
import json 
from IPython.core.display import HTML
import re
import sys
from __future__ import print_function

import helpers

# <codecell>

def paginate_tag_search(api, tag_search, max_results=40):
    results = []
    
    tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
    results += tag_recent_media    
    
    while len(results) < max_results:
        recs, next = api.tag_recent_media(tag_name=tag_search[0].name, with_next_url=next)
        results += recs  
        
    return results


def match_caption(media, pattern):
    """
    :media: an instagram Media object
    :pattern: a list of string patterns or a single string pattern
    
    :returns: bool
    """
    if media.caption is None:
        return False
    
    if (isinstance(pattern, list) or isinstance(pattern, tuple)):
        for pat in pattern:
            
            if re.search(pat, media.caption.text.lower()):
                return True
    else:
        if re.search(pattern, media.caption.text.lower()):
            return True
    return False


def has_tag(media, tag):
    """
    :media: an instagram Media object
    :tag: a list of tags as stings or a single string tag
    
    :returns: bool
    """
    if (isinstance(tag, list) or isinstance(tag, tuple)):
        for t in tag:
            if t in [tag.name for tag in media.tags]:
                return True
    else:
        if tag in [tag.name for tag in media.tags]:
            return True
        
    return False


def search_advanced(api, tag_primary, next=None, caption=None, tag=None, count=20, max_iters=20):
    if (caption is not None and tag is not None):
        raise ValueError, 'Perform either a caption or tag search'
        
    results = []
    iters = 0
    
    tag_search, next_tag = api.tag_search(q=tag_primary)
    if next is not None:
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name, with_next_url=next)
    else:
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
    iters += 1
    
    if caption is not None:
        for media in tag_recent_media:
            if match_caption(media, caption):
                results.append(media)
    if tag is not None:
        for media in tag_recent_media:
            if has_tag(media, tag):
                results.append(media) 
                
    while (len(results) < count and iters < max_iters):
        tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name, with_next_url=next)
        if caption is not None:
            for media in tag_recent_media:
                if match_caption(media, caption):
                    results.append(media)
        if tag is not None:
            for media in tag_recent_media:
                if has_tag(media, tag):
                    results.append(media) 
        iters += 1
        sys.stdout.write('\rPage %s - %s results found'%(iters, len(results)))
        sys.stdout.flush()
        
    #print '%s calls remaining'%api.x_ratelimit_remaining
    return results, next

# <codecell>

# Get your key/secret from http://instagram.com/developer/
with open(helpers.user_path('instagram_client_keys.txt'),'r') as fh:
    keys = json.load(fh)

# plop those babies in!
api = ig.client.InstagramAPI(client_id=keys['INSTAGRAM_CLIENT_ID'],
                   client_secret=keys['INSTAGRAM_CLIENT_SECRET'])

html_big = '<img src=%s width="600" />'
html_small = '<img src=%s width="200" />'
next_url=None

# <codecell>


results, next_url= search_advanced(api, tag_primary='twins', caption=['preg'], count=50, max_iters=500, next=next_url)

# <codecell>

html = ''
for media in results:
    html += html_small%media.images['standard_resolution'].url
    try:
        html += "<li>Caption: %s</li>"%media.caption.text
        html += "<li>Date: %s</li>"%media.created_time
        html += '''<li>Media: <a href="%s">Media</a></li>'''%media.link
        html += '''<a href="http://www.iconosquare.com/%s">%s</a></br>'''%(media.user.username, media.user.username)
    except:
        pass
HTML(html)

# <headingcell level=1>

# Scratchy

# <codecell>


# <codecell>

type(media.caption.text)

# <codecell>

res = paginate_tag_search(api, tag_search, 60)
html = ''
for media in res:
    html += html_small%media.images['standard_resolution'].url
    html += "<li>Caption: %s</li>"%media.caption
HTML(html)

# <codecell>

popular_media[0].tags
popular_media[0].link
popular_media[0].user.username

# <codecell>


#get popular images feed
popular_media = api.media_popular(count=40)

#extract urls of popular images to a list
photolist = []
for media in popular_media:
    photolist.append(media.images['standard_resolution'].url)

print 'Top photos from Instagram'
html = ''

#show the original image thumbnail
for p in photolist:
    html = html + '<img src=' + p + ' width="150" />'
from IPython.core.display import HTML
HTML(html)  

# <codecell>

type(popular_media[0].user)

# <codecell>

xx = popular_media[0].link

# <codecell>

xx

# <codecell>

popular_media[2].images['standard_resolution'].url

# <codecell>

print api.x_ratelimit

# <codecell>


