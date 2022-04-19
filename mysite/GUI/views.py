from django.shortcuts import render
import mimetypes
import os

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


