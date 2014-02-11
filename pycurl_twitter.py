# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import oauth2 as oauth

# <codecell>

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

# <codecell>

ck = 'kcYojLBeue9QwyMFjX5uWw'
cks = 'kckFWuXZ6CEVYuGTxVkgcMtaA3k6phQLHPXc0l3Klg'
at = '1126194344-cKj1hD5qzZA01muEilhyFujWcO5gtaRYfoslUI5'
ats = 'hPDctySk6tTjrRawDmpwaqFHMBjkbhPiPzlMDMSpI'

# <codecell>

base_url = 'https://api.twitter.com/1/account/verify_credentials.json'

# <codecell>

_signature_method_plaintext = oauth.SignatureMethod_PLAINTEXT()
_signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

_oauth_token    = oauth.Token(key=at, secret=ats)
_oauth_consumer = oauth.Consumer(key=ck, secret=cks)

# <codecell>

print _oauth_token, _oauth_consumer

# <codecell>


