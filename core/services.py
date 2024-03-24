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

    @staticmethod
    def complete_task(task_id, completion_reason):
        task = Task.objects.get(pk=task_id)
        task.completion_reason = completion_reason
        task.completion_datetime = timezone.now()
        task.save()
