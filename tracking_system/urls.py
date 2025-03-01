from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from tracking_system import views


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracking/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('task/', views.tasks, name='task'),
    path('new-task/', views.add_task, name='new-task'),
    path('task-detail/<int:task_id>/', views.task_detail, name='task-detail'),
    path('task/<int:task_id>/comment/', views.add_comment, name='task-comment'),
    path('task/<int:task_id>/comment/<int:comment_id>/like/', views.like_comment, name="like-comment"),
    path('task/<int:task_id>/comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike-comment'),
]
