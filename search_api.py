# -*- coding: utf-8 -*-
import requests_oauthlib
import requests
import json

token = {'TOKEN': "",
         'TOKEN_SECRET': "",
         'CONSUMER_KEY': "",
         'CONSUMER_SECRET': ""}


header_oauth = requests_oauthlib.OAuth1(token['CONSUMER_KEY'],
                                        token['CONSUMER_SECRET'],
                                        token['TOKEN'],
                                        token['TOKEN_SECRET'],
                                        signature_type='auth_header')

url = 'https://api.twitter.com/1.1/search/tweets.json?q=superbowl&result_type=recent&since_id=1&count=10'
response = requests.get(url, auth=header_oauth)

print(json.loads(response.text).keys())
tweets = json.loads(response.text)['statuses']

for tweet in tweets:
    print('==================')
    print(tweet['text'])
    #print(tweet['screen_name'])
    print(tweet['created_at'])
    print(tweet['id'])
