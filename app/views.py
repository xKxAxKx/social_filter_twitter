from requests_oauthlib import OAuth1Session
import json
import re
import os
import requests
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,
        'index.html',
    )

def tweet(tweet):
    pass
