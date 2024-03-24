from django import forms
from .models import Task


class CommentForm(forms.Form):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('IN_PROGRESS', 'In Progress'),
    ]
    comment_text = forms.CharField(label='Comment', widget=forms.Textarea)
    status = forms.ChoiceField(label='Status', choices=STATUS_CHOICES)
    

class TaskCompletionForm(forms.ModelForm):
    completion_reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Task
        fields = ['completion_reason']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'severity', 'deadline', 'assignee']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

