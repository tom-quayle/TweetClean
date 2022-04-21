from django import forms


class SearchTwitter(forms.Form):
    name = forms.CharField(label="Enter Your Twitter Name Here...", max_length=25)

    # this file can be deleted if we are not using Django's premade forms
