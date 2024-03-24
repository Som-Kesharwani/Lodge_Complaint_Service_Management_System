from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from django.utils import timezone

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_complete_task(self):
        task = Task.objects.create(title='Test Task', description='Test Description', priority='LOW',
                                   severity='LOW', deadline=timezone.now(), assignee=self.user)
        
        response = self.client.post(reverse('complete_task', kwargs={'task_id': task.id}),
                                    {'comment_text': 'Closing this', 'status': 'CLOSED'})
        
        self.assertEqual(response.status_code, 302)  # Redirect after adding a comment
       
        

    def test_add_comment(self):
        # Create a task
        task = Task.objects.create(title='Test Task', description='Test Description', priority='LOW',
                                   severity='LOW', deadline=timezone.now(), assignee=self.user)
        # Access the add comment page
        response = self.client.get(reverse('add_comment', kwargs={'task_id': task.id}))
        self.assertEqual(response.status_code, 200)
        print(response)

        # Post a comment
        response = self.client.post(reverse('add_comment', kwargs={'task_id': task.id}),
                                    {'comment_text': 'Test Comment', 'status': 'OPEN'})
        self.assertEqual(response.status_code, 302) 
        print(response)

        # Check if the comment is added to the task
        self.assertEqual(task.comment_set.count(), 1)
        print(response)

    def test_user_login(self):
        # Access the login page
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)
        print(response)

        # Login with valid credentials
        response = self.client.post(reverse('user_login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302) 
        print(response)

        # Logout
        response = self.client.get(reverse('user_logout'))
        self.assertEqual(response.status_code, 302) 
        print(response)