
# coding: utf-8

# In[16]:

class NetworkReadError(Exception):
    pass
class NetworkConnectionError(Exception):
    pass
class HttpInternalError(Exception):
    pass
class HttpRateLimitError(Exception):
    pass

def connect(consumer_key, consumer_secret, token, token_secret):
    import requests
    import requests_oauthlib
    auth = requests_oauthlib.OAuth1(consumer_key, consumer_secret, token, token_secret)
    try:
        r = requests.get('https://stream.twitter.com/1.1/statuses/sample.json',
                        stream = True,
                        auth = auth)
    except:
        raise NetworkConnectionError()        
    if r.status_code == 420:
        raise HttpRateLimitError()
    if r.status_code == 503:
        raise HttpInternalError()
    if r.status_code != 200:
        raise Exception("Un-expected http error status=%d" % r.status_code)
    return r


def read(r):
    import json, requests
    lines = r.iter_lines()
    while True:
        try:
            line = next(lines)
        except requests.exceptions.ConnectionError as e:
            raise NetworkReadError()
        if line:
            try:
                data = json.loads(line)
            except:
                raise Exception("Incorrect data received: %s" % line)
            yield data
def must_keep_tweet(tweet):
    if "retweeted_status" in tweet:
        return False
    return True


# In[18]:

r = connect(consumer_key = 'OcivAjJVUhZ3L5QEPWR3TEJSO', 
            consumer_secret='dUhh7pDUyMsODrChUkSlrV5JDJNRhtTAvams7gr96osiTmJcnI', 
            token = '399983938-kPOVoauPrqmzLNj2VflYGt0eDrDW4FXS0IRbMByd', 
            token_secret= 'An0Z8L6xFjfLufPlTPMWeXhJ5XxiyI0SttC4e0EwGqghJ')


# In[ ]:

import json
with open('sample.json', 'w') as o:
    for d in read(r):
        if not must_keep_tweet(d):
            continue
        o.write('%s\n' % json.dumps(d))
        o.flush()


# In[ ]:



