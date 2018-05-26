from django.contrib import admin
from .models import ProjectModel
from .models import DescriptionModel
from .models import StatusModel
from .models import TaskModel

admin.site.register(ProjectModel)
admin.site.register(StatusModel)
admin.site.register(DescriptionModel)


class TaskAdmin(admin.ModelAdmin):
    model = TaskModel
    filter_horizontal = ('description',)

admin.site.register(TaskModel, TaskAdmin)
