from django import forms


class SearchTwitter(forms.Form):
    name = forms.CharField(label="", max_length=25)

    # this file can be deleted if we are not using Django's premade forms
