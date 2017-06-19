#!/usr/bin/env python

import sys
import string
import simplejson
import pandas as pd
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import botometer


df1 = pd.read_csv('sosvenezuela_17-01.csv', sep= ';')
df2 = pd.read_csv('sosvenezuela_17-02.csv', sep= ';')
df3 = pd.read_csv('sosvenezuela_17-03.csv', sep= ';')
df4 = pd.read_csv('sosvenezuela_17-04.csv', sep= ';')
df5 = pd.read_csv('sosvenezuela_17-05.csv', sep= ';')

ids = df1.username #you can also use df['column_name']
ids2 = df2.username
ids3 = df3.username
ids4 = df4.username
ids5 = df5.username

ids = ids.append(ids2, ignore_index=True)
ids = ids.append(ids3, ignore_index=True)
ids = ids.append(ids4, ignore_index=True)
ids = ids.append(ids5, ignore_index=True)

ids = pd.Series(ids.unique())

ids = ids.sample(50)

CONSUMER_KEY = '5Rcxy0B6hTefj4WfI83Ov4rGn'
CONSUMER_SECRET = 'IROZKaE6Osnt7FlvVmZlWLEU9V1KT7TyZpda7CgrJKG5Qmtre5'
ACCESS_KEY = '86460420-9xJaN64nnrumh3QRJEfKWhTFcjf572kOtHGbRMkta'
ACCESS_SECRET = 'Rarw3wksqYiVDZsTMPebWDztDSuQuXSiIwfz40jgMkrsC'
auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.secure = True
api = tweepy.API(auth)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

#search
api = tweepy.API(auth)
twitterStream = Stream(auth,TweetListener())
desc = []

out = open("sosvenezuela_bios.csv", 'w')
out_bots = open("bots.csv", 'w')


mashape_key = "iykKYyk7XTmshsUERrKagp0XxruZp1mWfoEjsnS24G5TOEopR1"
twitter_app_auth = {
    'consumer_key': CONSUMER_KEY,
    'consumer_secret': CONSUMER_SECRET,
    'access_token': ACCESS_KEY,
    'access_token_secret': ACCESS_SECRET,
  }

bom = botometer.Botometer(mashape_key=mashape_key, **twitter_app_auth)



for user in ids:
    #print user
    try:
        info = api.get_user(screen_name = user)
        #desc.append(info.description)
        tweet = api.user_timeline(screen_name = user)
        result = bom.check_account(user)
        print(result['scores']['universal'])

        if result['scores']['universal'] < 0.5:
            inf = info.description
            
            # print((tweet[0].truncated))
            # print((tweet[0].text)) 
            # print((tweet[0].retweet_count.numerator))
            # print((tweet[0].retweet_count.denominator))

            # print(dir(tweet[0]))
            # print(dir(tweet[0].retweet.im_func.func_name))

            out.write(user + ",\"" + inf.rstrip("\n").encode('utf-8') + "\"\n")
            i = 1
            for t in tweet:
                inf = t.text
                out.write(str(i) + ",\"" + inf.rstrip("\n").encode('utf-8') + "\"\n")
                i += 1

        else:
            inf = info.description
            out_bots.write(user + ",\"" + inf.rstrip("\n").encode('utf-8') + "\"\n")
            i = 1
            for t in tweet:
                inf = t.text
                out_bots.write(str(i) + ",\"" + inf.rstrip("\n").encode('utf-8') + "\"\n")
                i += 1

    except Exception, e:
        print(user)
    

'''dataf = pd.DataFrame(np.column_stack([ids_s, desc]), 
                               columns=['username', 'description'])
dataf.to_csv("out.csv", sep=';')'''
out.close()
out_bots.close()

# for i in ids:
#     ids_s.append(i.partition(' ')[0])