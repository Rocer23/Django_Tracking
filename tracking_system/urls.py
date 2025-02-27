from django.urls import path
from django.contrib.auth import views as auth_views
from tracking_system import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('task/', views.tasks, name='task'),
    path('new-task/', views.add_task, name='new-task'),
    path('task-detail/<int:pk>/', views.task_detail, name='task-detail'),
]