# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import re
import os
import requests
import sys
import codecs
import pandas
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
from social_django.models import UserSocialAuth
import twitter
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from .forms import TweetForm

#形態素解析関連
import MeCab
mecab = MeCab.Tagger('-Ochasen')


PN_TXT = 'pn_ja.dic.txt'

pn_df = pandas.read_csv(PN_TXT,
                        sep=':',
                        encoding='utf-8',
                        names=('Word', 'Reading', 'POS', 'PN')
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
    social_account = UserSocialAuth.objects.get(user_id=request.user.id)
    user_oauth_token = social_account.extra_data['access_token']['oauth_token']
    user_oauth_token_sercret = social_account.extra_data['access_token']['oauth_token_secret']
    form = TweetForm

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = request.POST['tweet']

            tweet = tweet_post(tweet,
                               user_oauth_token,
                               user_oauth_token_sercret
                               )

            if tweet:
                message = '「{}」とツイートしました'.format(tweet)
            else:
                message = 'ツイートが失敗しました'

            form = TweetForm
            return render(request,
                          'home.html',
                          dict(account_name=account_name,
                               form=form,
                               message=message
                               )
                          )
    else:
        if request.user.is_authenticated():
            return render(request,
                          'home.html',
                          dict(account_name=account_name, form=form)
                          )
        else:
            return redirect('index')


#ツイートを形態素解析で分割する
def tweet_mecab_analysis(tweet):
    divided_tweet = mecab.parse(tweet)
    divided_tweet_split = divided_tweet.split('\n')  #形態素解析した文書を配列にする
    divided_tweet_lines = divided_tweet_split[0:-2]  # divided_tweet_splitから'EOS', ''を除去
    diclist = []
    for word in divided_tweet_lines:
        l = re.split('\t|,', word)
        d = {'Surface': l[0], 'POS1': l[1], 'POS2': l[2], 'POS3': l[3]}
        diclist.append(d)

    return(diclist)


# 形態素解析の結果をpnにマッチするように分割
def add_pnvalue(diclist_old):
    diclist_new = []
    for word in diclist_old:
        base = word['POS2']  #個々の辞書から基本形を取得
        if base in pn_dict:
            pn = float(pn_dict[base])
        else:
            pn = 'notfound'
        word['PN'] = pn
        diclist_new.append(word)
    return(diclist_new)


#ツイートのネガポジ値を判定する関数
def get_tweet_score(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        score = mean(pn_list)
    else:
        score = 0  # 全部notfoundならゼロにする
    return(score)


#平均値を出す関数
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


# twitterにポストする関数
def tweet_post(tweet, user_oauth_token, user_oauth_token_sercret):
    auth = twitter.OAuth(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                         consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                         token=user_oauth_token,
                         token_secret=user_oauth_token_sercret)
    t = twitter.Twitter(auth=auth)

    # ツイートのネガポジ判定&ツイートの差し替え
    # スコア値は微調整が必要だな...
    analyzed_tweet = tweet_mecab_analysis(tweet)
    tweet_pnvalue_list = add_pnvalue(analyzed_tweet)
    tweet_score = get_tweet_score(tweet_pnvalue_list)
    if tweet_score <= -0.50:
        tweet = "にゃーん"

    #実際にツイートしてみる
    # 例外が発生した場合、tweet=にゃーんだったらにゃーんを追加して再チャレンジ
    # にゃーん以外だったらNoneで返す(エラーの内容は問わず)
    try:
        t.statuses.update(status=tweet)
        return tweet
    except:
        if tweet.startswith("にゃーん"):
            for i in range(1, 10):
                if i == 10:
                    return None
                    break
                else:
                    tweet += "にゃーん"
                try:
                    t.statuses.update(status=tweet)
                    return tweet
                except:
                    continue
        else:
            return None
