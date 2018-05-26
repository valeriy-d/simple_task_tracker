from django.db.models import F
from django.views.generic import View
from django.shortcuts import get_object_or_404

from apps.utils import success_response
from apps.utils import json_required
from apps.utils import validate_fields

from .models import TaskModel
from .models import DescriptionModel

# Список алиасов для полей других моделей
aliases = {
    'project_id': F('project__id'),
    'status_id': F('status__id'),
    'author_id': F('author__id'),
    'doer_id': F('doer__id'),
    'project_name': F('project__name'),
    'status_name': F('status__name'),
    'author_name': F('author__username'),
    'doer_name': F('doer__username'),
}


class TaskListView(View):
    """
    Список задач без описаний
    """

    # @validate_fields(TaskModel)
    def get(self, request):


        # Фильтрация будет только по наименованиям
        # Добавим startswith для каждого параметра
        filters = {}
        for field, value in request.GET.items():
            filters.update({field + '__startswith': value})

        tasks = TaskModel.objects.all() \
                    .select_related('project', 'status', 'doer', 'author') \
                    .annotate(**aliases) \
                    .filter(**filters) \
                    .values('id', 'name', *aliases.keys())
        return success_response(records=list(tasks), totals=tasks.count())


class TaskDescriptionView(View):
    """
    Получить/добавить/удалить комментарии для определенной задачи
    """
    def get(self, request, task_id):
        descriptions = DescriptionModel.objects.filter(taskmodel__id=task_id) \
                                               .annotate(taskmodel_id=F("taskmodel__id")) \
                                               .values('text', 'taskmodel_id')
        return success_response(records=list(descriptions))

    @json_required('text')
    def post(self, request, task_id):
        data = request.json_data
        print(task_id)
        task = TaskModel.objects.get(id=task_id)
        description = task.description.create(text=data.get('text', ''))
        return success_response(id=description.id)


class CreateTaskView(View):
    """
    Создать задачу

    POST /task "json/application" {name: <str>, author_id: <int>, doer_id: <int>, project_id: <int>, status_id: <int>}
    """
    http_method_names = ['post', ]

    @json_required('name', 'author_id', 'doer_id', 'project_id', 'status_id')
    def post(self, request):
        data = request.json_data
        print(data)
        task = TaskModel.objects.create(**data)
        task = TaskModel.objects.select_related('project', 'status', 'doer', 'author') \
                   .filter(id=task.id) \
                   .annotate(**aliases) \
                   .values('id', 'name', *aliases.keys())
        return success_response(status=True, task=list(task)[0])


class ChangeTaskView(View):
    def _get_task(self, task_id):
        return get_object_or_404(TaskModel, id=task_id)

    def delete(self, request, task_id):
        task = self._get_task(task_id)
        task.delete()
        return success_response()

    @json_required()
    @validate_fields(TaskModel)
    def patch(self, request, task_id):
        data = request.json_data
        task = TaskModel.objects.filter(id=task_id)
        task.update(**data)
        task = task.select_related('project', 'status', 'doer', 'author') \
                    .annotate(**aliases) \
                    .values('id', 'name', *aliases.keys())

        return success_response(task=list(task)[0])
