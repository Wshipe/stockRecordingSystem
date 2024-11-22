from django.shortcuts import render
from django.http import HttpResponse
from . import views

# Create your views here.

def home(request):
    return render(request, 'index.html')
