from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # URL for task list
    path('create/', views.create_task, name='create_task'),  # URL for creating a task
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),  # URL for completing a task
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('tasks/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),

    # Add more URL patterns as needed
]
