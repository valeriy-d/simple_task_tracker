from django.urls import path

from .views import CreateTaskView
from .views import TaskListView
from .views import TaskDescriptionView
from .views import ChangeTaskView

urlpatterns = [
    path(r'task', CreateTaskView.as_view(), name='create_task'),
    path(r'task/list', TaskListView.as_view(), name='task_list'),
    path(r'task/descr/<int:task_id>', TaskDescriptionView.as_view(), name='description'),
    path(r'task/<int:task_id>', ChangeTaskView.as_view(), name='task_change'),
]