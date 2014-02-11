# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
import tweepy
import sys
ck = 'kcYojLBeue9QwyMFjX5uWw'
cks = 'kckFWuXZ6CEVYuGTxVkgcMtaA3k6phQLHPXc0l3Klg'
at = '1126194344-cKj1hD5qzZA01muEilhyFujWcO5gtaRYfoslUI5'
ats = 'hPDctySk6tTjrRawDmpwaqFHMBjkbhPiPzlMDMSpI'



auth = tweepy.OAuthHandler(ck, cks)
api = tweepy.API(auth)

# <codecell>

braves = api.get_user('Braves')

# <codecell>

brave_friends = [friend for friend in braves.friends()]

print len(brave_friends)
#for f in brave_friends: print f

# <codecell>

# Iterate through the first 200 statuses in the friends timeline
bra = api.get_user('Braves')
print bra.friends()

for xx in tweepy.Cursor(bra.friends()).items(200):
    # Process the status here
    print xx.screen_name

# <codecell>


