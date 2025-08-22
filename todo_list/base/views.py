from django.shortcuts import render
from django.http import HttpResponse
from .models import Task

# Create your views here.

def home(request):
    tasks = Task.objects.all()
    context = {"tasks":tasks}
    return render(request,'base/home.html',context)
