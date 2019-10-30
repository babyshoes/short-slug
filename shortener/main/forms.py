from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label="Long URL")

class CustomURLForm(forms.Form):
    url = forms.URLField(label="Long URL")
    short = forms.SlugField(label="Short URL")