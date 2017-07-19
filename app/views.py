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

def index(request):
    return render(request,
        'index.html',
    )


@login_required
def home(request):
    if request.user.is_authenticated():
        account_name = request.user.username
    else:
        account_name = None

    return render(request,
        'home.html',
        {"account_name": account_name}
    )


def logout(request):
    return render(request,
        'logout.html',
    )
