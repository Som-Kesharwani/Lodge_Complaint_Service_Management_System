# services.py
from .models import Task
from django.utils import timezone

class TaskService:
    @staticmethod
    def create_task(title, description, priority, severity, deadline, assignee):
        return Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            severity=severity,
            deadline=deadline,
            assignee=assignee
        )

