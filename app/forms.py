from django import forms
import os
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError

class TweetForm(forms.Form):
    tweet = forms.CharField(label="tweet", widget=forms.Textarea, max_length = 140, error_messages={'required': "なんかおかしいっす"}))
