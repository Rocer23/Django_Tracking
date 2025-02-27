from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from tracking_system.models import Task, Comments
from django.http import HttpResponse
from django.contrib.auth import login


# Create your views here.

def index(request):
    tasks = Task.objects.all()
    return render(request, template_name='tracking/index.html', context={'tasks': tasks})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, template_name='tracking/register.html', context={'form': form})


def tasks(request):
    task = Task.objects.all()
    return render(request, template_name='tracking/task.html', context={'task': task})


# Додавання нового Завдання(Task)
def add_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            start = request.POST.get('start')
            end = request.POST.get('end')
            status = request.POST.get('status') == 'on'
            prioritet = request.POST.get('prioritet', 1)
            permission = request.POST.get('permission') == 'on'

            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                start=start,
                end=end,
                status=status,
                prioritet=prioritet,
                permission=permission
            )
            return redirect('task')

        return render(request, template_name='tracking/add_task.html')
    else:
        return redirect('login')


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    comments = Comments.objects.filter(task=task)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comments.objects.create(user=request.user, task=task, comment=comment)
        return redirect('task-detail', pk=pk)
    return render(request, template_name='tracking/task_detail.html', context={'task': task, 'comments': comments})
