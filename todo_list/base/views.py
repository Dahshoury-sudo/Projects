from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task,User
from .forms import TaskForm

# Create your views here.

def home(request):
    tasks = Task.objects.all()
    context = {"tasks":tasks}
    return render(request,'base/home.html',context)


def addtask(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('home')

    context = {'form':form}
    return render(request,'base/add_task.html',context)

def showtask(request,pk):
    task = Task.objects.get(id=pk)
    context = {'task':task}
    return render(request,'base/task.html',context)


def deletetask(request,pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        # task.delete()
        task.completed = True
        return redirect('home')
    context = {'obj':task}
    return render(request,'base/delete.html',context)