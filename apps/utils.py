import json
from functools import wraps

from django.http import JsonResponse
from django.http import HttpResponseBadRequest

def success_response(**kwargs):
    response = {"success": True}
    response.update(kwargs)
    return JsonResponse(response)

def json_required(*args):
    """
    Устанавливает необходимость json данных для запроса
    записывает результат в request.json_data
    иначе BadRequest 400
    """
    def func_wrapper(func):
        @wraps(func)
        def wrapper(self, request, *func_args, **func_kwargs):
            try:
                request.json_data = json.loads(request.body)
            except Exception as e:
                return HttpResponseBadRequest()
            else:
                # проверяем переданные параметры, если надо
                if args:
                    rfields = request.json_data.keys()
                    if len(set(args) & set(rfields)) != len(args):
                        return HttpResponseBadRequest()

                return func(self, request, *func_args, **func_kwargs)
        return wrapper
    return func_wrapper

def validate_fields(model):
    """
    Проверка на соответствие переданных полей
    полям модели
    :param model: класс модели
    """
    def func_wrapper(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            rfields = request.json_data.keys()
            fields = [f.name for f in model._meta.get_fields()]

            # если в запросе переданы поля отличающиеся от полей модели, то ошибка
            if len(set(fields) | set(rfields)) > len(fields):
                return HttpResponseBadRequest()
            else:
                return func(self, request, *args, **kwargs)
        return wrapper
    return func_wrapper
