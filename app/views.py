from requests_oauthlib import OAuth1Session
import json
import re
import os
import requests
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import TweetForm

def index(request):
    return render(request,
        'index.html',
    )


@login_required
def home(request):
    if request.user.is_authenticated():
        account_name = request.user.username
        form = TweetForm
        return render(request,
            'home.html',
            dict(account_name = account_name, form = form)
        )
    else:
        return redirect('index')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        tweet = request.POST['tweet']
        import pdb; pdb.set_trace()

# ツイートを解析し、数値でネガティブ値を取得する
def tweet_analysis(tweet):
    pass


# 実際にtwitterにポストする関数
def tweet(tweet):
    pass
