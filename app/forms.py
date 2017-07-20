from django import forms
import os
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError

class TweetForm(forms.Form):
    tweet = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'なんであいつのために俺が苦労しないといけないんだ'}),
        max_length = 140,
        error_messages={'required': "なんかおかしいっす"})
