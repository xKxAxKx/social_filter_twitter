# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import re
import os
import requests
import sys, codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import TweetForm

# 形態素解析関連
import MeCab
mecab = MeCab.Tagger('-Ochasen')


def index(request):
    return render(request,
        'index.html',
    )


@login_required
def home(request):
    account_name = request.user.username
    form = TweetForm

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = request.POST['tweet']

            analyzed_tweet = tweet_mecab_analysis(tweet)

            return render(request,
                'home.html',
                dict(account_name = account_name, form = form, tweet = tweet)
            )
    else:
        if request.user.is_authenticated():
            return render(request,
                'home.html',
                dict(account_name = account_name, form = form)
            )
        else:
            return redirect('index')


# ツイートを形態素解析で分割する
def tweet_mecab_analysis(tweet):
    divided_tweet = mecab.parse(tweet)
    divided_tweet_lines = divided_tweet.split('\n')
    divided_tweet_lines = divided_tweet_lines[0:-2]
    diclist = []
    for word in divided_tweet_lines:
        l = re.split('\t|,',word)
        d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[3]}
        diclist.append(d)
    return(diclist)


# twitterにポストする
def tweet(tweet):
    pass
