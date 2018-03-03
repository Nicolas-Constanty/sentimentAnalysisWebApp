#!/usr/bin/env python3

import tweepy
import os
import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
import time

nltk.download('vader_lexicon')
init_notebook_mode(connected=True)

consumer_key = os.environ['APP_KEY']
consumer_secret = os.environ['APP_KEY_SECRET']
access_token = ""
access_token_secret = ""

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

def search(searchQuery, maxTweets=10000, tweetsPerQry=100, fName='tweets.txt', display=False):
    start_time = time.time()
    data_all = []

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'w', encoding='utf-8', errors='ignore') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    f.write(tweet._json['text'] + '\n')
                    data_all.append(tweet._json['text'])
                tweetCount += len(new_tweets)
                if (display):
                    print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break
    print("--- %s seconds ---" % (time.time() - start_time))
    return { "data": data_all, "query": searchQuery }

def analyseTweets(tweets, display=False):
    sia = SIA()
    pos_list = []
    neg_list = []
    neu_list = []
    for post in tweets["data"]:
        res = sia.polarity_scores(post)
        if (display):
            print(res)

        if res['compound'] > 0.2:
            pos_list.append(post)
        elif res['compound'] < -0.2:
            neg_list.append(post)
        else:
            neu_list.append(post)
    return { "positives" : pos_list, "negatives" : neg_list, "neutrals" : neu_list, "query" : tweets["query"] }
