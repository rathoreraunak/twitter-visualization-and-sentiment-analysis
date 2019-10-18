from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import userinput, userinputtext
import sentimeter


def index(request):
    user_input = userinput()
    user_input1 = userinputtext()
    return render(request, "index.html", {'input_hastag': user_input, 'input_hastag1': user_input1})


def getTrends(request):
    user_input = userinput()
    user_input1 = userinputtext()
    return render(request, "getTrends.html", {'input_hastag': user_input, 'input_hastag1': user_input1})


def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        print(input_hastag)
        data = primary(request, input_hastag)
        return render(request, "result.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})


def analyseSingle(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        print(input_hastag)
        data = primarySingle(request, input_hastag)
        return render(request, "result.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})

def analysesingle_user(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        print(input_hastag)
        data = primary(request, input_hastag)
        return render(request, "result.html", {'data': data})
    return render(request, "index.html", {'input_hastag': user_input})


from secrets import Oauth_Secrets
import tweepy
from textblob import TextBlob


def primary(request, input_hashtag):
    secrets = Oauth_Secrets()  # secrets imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)

    N = 10  # Number of Tweets
    Tweets = tweepy.Cursor(api.search, q=input_hashtag,lang='en').items(N)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    print('hello')
    mydictionary = {"tweets": []}
    tweet1 = mydictionary["tweets"]
    for tweet in Tweets:
        print (tweet.text)
        print (tweet.user.screen_name)
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:  # Negative
            neg += blob.sentiment.polarity
            output = 'Negative'
            neg_count += 1
        elif blob.sentiment.polarity == 0:  # Neutral
            neutral_count += 1
            output = 'Neutral'
        else:  # Positive
            pos += blob.sentiment.polarity
            pos_count += 1
            output = 'Positive'
        tweet1.append({"tweet": tweet.text, "output": output,"name": tweet.user.name,"id":tweet.user.screen_name})

    request.session['listvalue'] = tweet1
    # print "Total tweets",N
    # print "Positive ",float(pos_count/N)*100,"%"
    # print "Negative ",float(neg_count/N)*100,"%"
    # print "Neutral ",float(neutral_count/N)*100,"%"
    return [['Sentiment', 'no. of tweets'], ['Positive', pos_count]
        , ['Neutral', neutral_count], ['Negative', neg_count]]

def primaryUser(request, input_hashtag):
    secrets = Oauth_Secrets()  # secrets imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)

    N = 10  # Number of Tweets
    Tweets = tweepy.Cursor(api.search, q=input_hashtag,lang='en').items(N)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    mydictionary = {"tweets": []}
    tweet1 = mydictionary["tweets"]
    for tweet in Tweets:
        print (tweet.text)
        print (tweet.user.screen_name)
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:  # Negative
            neg += blob.sentiment.polarity
            output = 'Negative'
            neg_count += 1
        elif blob.sentiment.polarity == 0:  # Neutral
            neutral_count += 1
            output = 'Neutral'
        else:  # Positive
            pos += blob.sentiment.polarity
            pos_count += 1
            output = 'Positive'
        tweet1.append({"tweet": tweet.text, "output": output,"name": tweet.user.name,"id":tweet.user.screen_name})

    request.session['listvalue'] = tweet1
    # print "Total tweets",N
    # print "Positive ",float(pos_count/N)*100,"%"
    # print "Negative ",float(neg_count/N)*100,"%"
    # print "Neutral ",float(neutral_count/N)*100,"%"
    return [['Sentiment', 'no. of tweets'], ['Positive', pos_count]
        , ['Neutral', neutral_count], ['Negative', neg_count]]

def getWoeidView(request):
    data = getWoeidInternal(request)
    return render(request, "getTrends.html", {'data': data})


def getWoeidInternal(request):
    secrets = Oauth_Secrets()  # secrets imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)
    places = api.trends_available()
    for place in places:
        # Process a single status
        print(place)
    request.session['lstWoeid'] = places
    return places


def getCurrentTrends(request, woeid):
    print (woeid)
    trends = getTrendBasedOnWoeid(request, woeid)

    return render(request, "getCurrentTrends.html", {'data': trends})


import json


def getTrendBasedOnWoeid(request, woeid):
    secrets = Oauth_Secrets()  # secrets imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)
    mydictionary = {"trends": []}
    tweet = mydictionary["trends"]
    api = tweepy.API(auth)
    trends = api.trends_place(woeid)

    for resp in trends:
        for trend in resp['trends']:
            tweet.append({"name": trend['name'], "url": trend['url']}, )
    request.session['trends']=tweet

    return tweet


def primarySingle(request, input_hashtag):
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    print (input_hashtag)

    blob = TextBlob(input_hashtag)
    mydictionary = {"tweets": []}
    tweet = mydictionary["tweets"]

    if blob.sentiment.polarity < 0:  # Negative
        neg += blob.sentiment.polarity
        neg_count += 1
        output = 'Negative'
    elif blob.sentiment.polarity == 0:  # Neutral
        neutral_count += 1
        output = 'Neutral'
    else:  # Positive
        pos += blob.sentiment.polarity
        pos_count += 1
        output = 'Positive'

    tweet.append({"tweet": input_hashtag, "output": output})

    request.session['listvalue'] = tweet

    # print "Total tweets",N
    # print "Positive ",float(pos_count/N)*100,"%"
    # print "Negative ",float(neg_count/N)*100,"%"
    # print "Neutral ",float(neutral_count/N)*100,"%"
    return [['Sentiment', 'no. of tweets'], ['Positive', pos_count]
        , ['Neutral', neutral_count], ['Negative', neg_count]]
