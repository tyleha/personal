# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import praw
import time 


# <codecell>

lookbackTime = time.mktime(time.gmtime()) - 60*60*48# should be sys.argv[1] at some point
r = praw.Reddit(user_agent='some_kind_of_bot')

subredditName = 'python'
sub = r.get_subreddit(subredditName)

posts = [p for p in sub.get_new(limit=25)]
while posts[-1].created_utc > lookbackTime:
    posts += [p for p in sub.get_new(params={"after":posts[-1].name})]

for p in posts:
    print p.score, p.title

# <codecell>


