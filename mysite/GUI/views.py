from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

def index(request):
    return HttpResponse('hello world')

def FAQs(request):
    return render(request,'GUI/FAQsPage.html')

def Manual(request):
    return render(request,'GUI/ManualPage.html')

def Results(request):
    return render(request,'GUI/ResultsPage.html')

def Search(request):
    return render(request,'GUI/SearchPage.html')
