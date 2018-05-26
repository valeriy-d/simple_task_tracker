from django.db import models
from django.contrib.auth.models import User


class StrRepr:
    def __str__(self):
        return self.name


class ProjectModel(StrRepr, models.Model):
    name = models.CharField('Название проекта', max_length=255)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class StatusModel(StrRepr, models.Model):
    name = models.CharField('Название статуса', max_length=255)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class DescriptionModel(models.Model):
    text = models.TextField('Описание', max_length=5000)

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'

    def __str__(self):
        return self.text[:20]


class TaskModel(models.Model):
    name = models.CharField('Название задачи', max_length=255)
    project = models.ForeignKey('ProjectModel', on_delete=None)
    status = models.ForeignKey('StatusModel', on_delete=None)
    doer = models.ForeignKey(User, related_name='doer', on_delete=None)
    author = models.ForeignKey(User, related_name='author', on_delete=None)
    description = models.ManyToManyField(DescriptionModel)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return '%(name)s <status=%(status)s project=%(project)s>' % \
               {"name": self.name, "status": self.status, "project": self.project}
