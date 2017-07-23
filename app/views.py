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
import pandas as pd
# pn_ja.dic.txtはフルパスで指定
pn_df = pd.read_csv('/Users/user/Dev/kakutani/social_filter_twitter/app/pn_ja.dic.txt',\
                    sep=':',
                    encoding='utf-8',
                    names=('Word','Reading','POS', 'PN')
                   )
# PN Tableをデータフレームからdict型に変換しておく
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])  # 中身の型はnumpy.float64
pn_dict = dict(zip(word_list, pn_list))

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
            tweet_pnvalue_list = add_pnvalue(analyzed_tweet)
            tweet_score = get_tweet_score(tweet_pnvalue_list)
            print(tweet_score)

            if tweet_score == -0.41375900000000004 or tweet_score <= -0.661141:
                tweet = "にゃーん"

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


def add_pnvalue(diclist_old):
    diclist_new = []
    for word in diclist_old:
        base = word['POS2'] # 個々の辞書から基本形を取得
        if base in pn_dict:
            pn = float(pn_dict[base])
        else:
            pn = 'notfound'
        word['PN'] = pn
        diclist_new.append(word)
    return(diclist_new)


def get_tweet_score(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        score = mean(pn_list)
    else:
        score = 0 # 全部notfoundならゼロにする
    return(score)


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


# twitterにポストする
def tweet(tweet):
    pass
