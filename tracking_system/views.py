from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import View

from tracking_system.models import Task, Comments
from .forms import CommentForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login

from .mixin import OwnershipRequiredMixin


# Create your views here.

def index(request):
    task = Task.objects.all()
    other_task = Task.objects.all()
    return render(request, template_name='tracking/index.html', context={'tasks': task, 'other_task': other_task})


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


# User
def user(request):
    user = User.objects.all()
    return render(request, template_name='tracking/user.html', context={'user': user})


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


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    comments = Comments.objects.filter(task=task)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comments.objects.create(user=request.user, task=task, comment=comment)
        return redirect('task-detail', id=task_id)
    return render(request, template_name='tracking/task_detail.html', context={'task': task, 'comments': comments})


def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        # print("POST дані:", request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()

            return JsonResponse({
                "user": request.user.username,
                "text": comment.text,
                "created_at": comment.created_at.strftime("%Y-%m_%d %H:%M")
            })
        # print("Помилка валідації форми:", form.errors)
        return JsonResponse({"error": "Invalid request"}, status=400)


def like_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    if request.method == "POST":
        comment.likes += 1
        comment.save()
        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

    return JsonResponse({"error": "Invalid request"}, status=400)


def dislike_comment(request, task_id, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    if request.method == "POST":
        comment.dislikes += 1
        comment.save()
        return JsonResponse({"likes": comment.likes, "dislikes": comment.dislikes})

    return JsonResponse({"error": "Invalid request"}, status=400)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if comment.user != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    comment.delete()

    return JsonResponse({"message": "Comment deleted successfully"})


def other_tasks(request, task_id):
    other_task = Task.objects.exclude(user=request.user).exclude(id=task_id)
    return render(request, template_name='tracking/task_detail.html', context={'other_tasks': other_task})


class EditCommentView(LoginRequiredMixin, OwnershipRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        new_text = request.POST.get("text")
        if new_text:
            self.comment.text = new_text
            self.comment.save()
            return JsonResponse({"message": "Comment updated", "text": self.comment.text})
        return JsonResponse({"error": "Text field cannot be empty"}, status=400)


class DeleteCommentView(LoginRequiredMixin, OwnershipRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        self.comment.delete()
        return JsonResponse({"Message": "Comment deleted"})
