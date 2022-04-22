from django.shortcuts import render
import mimetypes
import os

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .forms import SearchTwitter # delete if not using forms.py
from .Web_Crawler import twitterCrawl
from .sentiment import AiSentiment

def index(request):
    return HttpResponse('hello world')

def FAQs(request):
    return render(request,'GUI/FAQsPage.html')

def Manual(request):
    return render(request,'GUI/ManualPage.html')

def Results(request):
    name = request.GET['name']
    SelfObject = twitterCrawl(v2=True)
    SelfObject.search_tweets_v2('"{}" lang:en'.format(name))
    AIObject = AiSentiment()
    AIObject.excactResults(SelfObject.results)
    neutral = len(AIObject.data['Neutral'])
    negative = len(AIObject.data['Negative'])
    positive = len(AIObject.data['Positive'])
    return render(request,'GUI/ResultsPage.html', {"PositiveSearchResults": positive, "NegativeSearchResults": negative, "NeutralSearchResults": neutral, "SearchTerm": name}) # name is placeholder until we implement AI

def Search(request):
    form = SearchTwitter() # have Django make a premade form for us?
    return render(request,'GUI/SearchPage.html', {"form": form}) # have Django make a premade form for us?

def download_file(request, filename=''):
    if filename != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/GUI/Files/' + filename
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    else:
        return render(request, 'GUI/ManualPage.html')


