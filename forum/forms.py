from django.forms import ModelForm
from django import forms
from .models import Thread, Post


class AddThread(forms.Form):
    title = forms.CharField(max_length=170)
    type_ = forms.ChoiceField(
        choices=(('NM', 'Normal'), ('PN', 'Pinned'), ('AM', 'Announcement')))
    post = forms.CharField(widget=forms.Textarea)
    

class AddPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
