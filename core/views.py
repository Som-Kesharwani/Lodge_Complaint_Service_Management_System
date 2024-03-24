from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import TaskForm, LoginForm, TaskCompletionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .services import TaskService
from .models import Task, Comment
from django.urls import reverse
from .forms import CommentForm

@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task_id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            status = form.cleaned_data['status']

            # Create the comment associated with the task and the current user
            Comment.objects.create(task=task, user=request.user, comment_text=comment_text)
            # Update the task status
            
            return redirect(reverse('add_comment', kwargs={'task_id': task_id}))
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'task': task,'comments': comments})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')  # Redirect to task list page after successful login
            else:
                # Invalid login
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user_login') 


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    print(request)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            status = form.cleaned_data['status']
            task.completion_reason=comment_text
            task.status = status
            task.completion_datetime=timezone.now()
            task.save()
    return redirect('task_list')
    


@login_required
def task_list(request):
    if request.user.is_authenticated:
        # User is logged in
        print("User is logged in")
        print("Username:", request.user.username)
        if request.user.is_superuser:  # Check if the user is an admin
            tasks = Task.objects.all()
        else:
            # Get tasks assigned to the current user
            tasks = Task.objects.filter(assignee=request.user)
        return render(request, 'task_list.html', {'tasks': tasks})
    else:
        # User is not logged in
        print("User is not logged in")
        return redirect(reverse('login'))

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = TaskService.create_task(
                form.cleaned_data['title'],
                form.cleaned_data['description'],
                form.cleaned_data['priority'],
                form.cleaned_data['severity'],
                form.cleaned_data['deadline'],
                form.cleaned_data['assignee']
            )
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})
