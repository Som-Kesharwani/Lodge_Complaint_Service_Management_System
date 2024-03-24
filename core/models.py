from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 



class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    Status_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Close'),
        ('IN_PROGRESS', 'In Progress'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=Status_CHOICES, default='OPEN')
    deadline = models.DateTimeField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(default=timezone.now)
    completion_reason = models.CharField(max_length=200, blank=True, null=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"