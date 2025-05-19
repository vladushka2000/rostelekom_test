from functools import wraps

from flask import request

from interfaces import base_schema


def validate_request(model: type[base_schema.BaseWebSchema]):
    """
    Отвалидировать body-запроса
    :param model: Pydantic-модель для валидации
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validated_data = model(**request.json)

            return f(data=validated_data, *args, **kwargs)

        return wrapper

    return decorator
