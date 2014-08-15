# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import instagram as ig
import numpy as np
import matplotlib.pyplot as plt
import json 
from IPython.core.display import HTML

import helpers

# <codecell>

# Get your key/secret from http://instagram.com/developer/
with open(helpers.user_path('instagram_client_keys.txt'),'r') as fh:
    keys = json.load(fh)

# plop those babies in!
api = ig.client.InstagramAPI(client_id=keys['INSTAGRAM_CLIENT_ID'],
                   client_secret=keys['INSTAGRAM_CLIENT_SECRET'])

html_big = '<img src=%s width="600" />'
html_small = '<img src=%s width="200" />'

# <codecell>

tag_search, next_tag = api.tag_search(q='nose', count=40)
tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
print 'found %s results'%len(tag_recent_media)

# <codecell>

cap, next = api.tag_recent_media(tag_name=tag_search[0].name, with_next_url=next)

# <codecell>

html = ''
for media in tag_recent_media:
    html += html_small%media.images['standard_resolution'].url
    html += "<li>Caption: %s</li>"%media.caption
HTML(html)

# <codecell>

html = ''
for media in cap[1:]: #first element is same as last of prev???
    html += html_small%media.images['standard_resolution'].url
    html += "<li>Caption: %s</li>"%media.caption
HTML(html)

# <codecell>

cap

# <codecell>


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


