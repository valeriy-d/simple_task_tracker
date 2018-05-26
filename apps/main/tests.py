import json
from random import randint
from functools import partial

from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User

from .models import TaskModel
from .models import ProjectModel
from .models import StatusModel
from .models import DescriptionModel

test_projects = [
    'ФУКУСИМА 2.0',
    'Скрытые возможности',
    'Шоколадная фабрика'
]

test_statuses = [
    'Новый',
    'В работе',
    'Приостановлена',
    'Отменена',
    'Завершена'
]

test_users = [
    'good_user',
    'bad_user',
    'simple_user',
    'author',
    'infinite_doer',
]

task_names = [
    'Вынести мусор',
    'Построить мост',
    'Убить Билла',
    'Придумать сложную загадку первокласснику'
]

def json_request(method, *args, **kwargs):
    kwargs.update({'content_type': 'application/json'})
    kwargs['data'] = json.dumps(kwargs.get('data', {}))
    print(method, args, kwargs)
    return method(*args, **kwargs)


class TaskTestCase(TestCase):
    def _get_rand_objects(self):
        return {
            'project': ProjectModel.objects.order_by('?').first(),
            'status': StatusModel.objects.order_by('?').first(),
            'author': User.objects.order_by('?').first(),
            'doer': User.objects.order_by('?').first(),
        }

    def _create_task(self):
        name = task_names[randint(0, len(task_names) - 1)]
        return TaskModel.objects.create(name=name, **self._get_rand_objects())

    def _create_records(self, test_data, model, field):
        for data in test_data:
            model.objects.create(**{field: data})

    def setUp(self):
        self.c = Client()
        # Создаем пользователей, проекты, статусы
        data = [
            (test_users, User, 'username'),
            (test_projects, ProjectModel, 'name'),
            (test_statuses, StatusModel, 'name')
        ]

        for args in data:
            self._create_records(*args)

        self._create_task()

    def test_task_list(self):
        response = self.c.get('/task/list')
        self.assertEqual(response.status_code, 200)

    def test_success_creating_task(self):
        """
        Переданы корректные паараметры, на выходе должны получить
        json данные о новой задаче
        """
        task_info = self._get_rand_objects()
        params = {}
        for key, value in task_info.items():
            params.update({key + '_id': value.id})

        params.update({'name': task_names[randint(0, len(task_names) - 1)]})
        response = json_request(self.c.post, '/task', data=params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._headers.get('content-type', None), ('Content-Type', 'application/json'))

        data = response.json()
        data_task = data.get('task')
        task_id = data_task.get('id', None)

        try:
            task_id = int(task_id)
        except ValueError as e:
            self.assertTrue(False, 'Incorrect id')

        task = TaskModel.objects.get(id=task_id)

        self.assertIsNotNone(task, 'There is no task was sanded to creating')
        self.assertEqual(task.name, params.get('name'))

    def test_failure_creating_task(self):
        """
        Переданы не все параметры и/или параметры,
        которых нет в списке требуемых
        """
        bad_params = {
            "name": 'Плохая задача',
            "bad_field": 'anything'
        }

        response = json_request(self.c.post, '/task', data=bad_params)

        self.assertEquals(response.status_code, 400)

    def test_success_change_task(self):
        new_name = 'Changed name'
        task = TaskModel.objects.order_by('?').first()
        params = {
            "name": new_name
        }
        # response = self.c.patch('/task/%d' % task.id, json.dumps(params), content_type='application/json')
        response = json_request(self.c.patch, '/task/%d' % task.id, data=params)
        print(response)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data.get('task', None))
        data_task = data.get('task', None)
        self.assertEqual(new_name, data_task.get('name', 'Bad name'))

        new_task = TaskModel.objects.get(id=data_task.get('id'))
        self.assertEquals(new_task.name, new_name)

    def test_failure_change_task(self):
        task = TaskModel.objects.order_by('?').first()
        bad_params = {
            "task_name": "Whatever"
        }
        response = json_request(self.c.patch, '/task/%d' % task.id, data=bad_params)
        self.assertEquals(response.status_code, 400)

    def test_getting_task_description(self):
        task = self._create_task()
        response = self.c.get('/task/descr/%d' % task.id)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response._headers.get('content-type', None), ('Content-Type', 'application/json'))

    def test_add_task_description(self):
        task = self._create_task()
        params = {
            "text": "New description"
        }

        response = json_request(self.c.post, '/task/descr/%d' % task.id, data=params)

        self.assertEquals(response.status_code, 200)
        data = response.json()

        description = DescriptionModel.objects.filter(id=data.get('id', None)).first()

        self.assertIsNotNone(description)
        self.assertEquals(description.text, params.get("text"))
