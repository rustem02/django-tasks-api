from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='api', password='api')

    def auth(self):
        resp = self.client.post('/api/token/', {'username':'api','password':'api'}, format='json')
        self.assertEqual(resp.status_code, 200)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_tasks(self):
        Task.objects.create(title='A')
        resp = self.client.get('/api/tasks')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('results', resp.data)
        self.assertEqual(resp.data['count'], 1)

    def test_create_requires_auth(self):
        resp = self.client.post('/api/tasks', {'title':'X'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_and_crud_flow(self):
        self.auth()
        # create
        resp = self.client.post('/api/tasks', {'title':'Demo','description':'T','status':'pending'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        task_id = resp.data['id']

        # retrieve
        resp = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], 'Demo')

        # update
        resp = self.client.put(f'/api/tasks/{task_id}', {'title':'Updated','status':'in_progress'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['status'], 'in_progress')

        # delete
        resp = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(resp.status_code, 204)

    def test_validation_title_required(self):
        self.auth()
        resp = self.client.post('/api/tasks', {'title':'   '}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('title', resp.data)
