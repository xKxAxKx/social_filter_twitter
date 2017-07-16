from requests_oauthlib import OAuth1Session
import json
import re
import os
import requests
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class index(TemplateView):
    template_name = "index.html"


class home(TemplateView):
    pass


def login(request):
    pass


def tweet(request):
    pass
