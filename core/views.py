from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse 

from .models import *


# Create your views here.
class Index(View):
    def get(self, request):

        return render(request, 'index.html') 