import uuid
import importlib

from django.db import models
from django.contrib.contenttypes.models import ContentType


class CalculatedField():
    def __init__(self, function, field_name=None):
        self.function = function
        if field_name is None:
            self.field_name = function.__name__[1:]
        else:
            self.field_name = field_name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        else:
            return self.function(obj)

    def __set__(self, obj, value):
        raise AttributeError("Read only field")

    def __str__(self):
        return self.field_name


def calculated_field(_handlers):
    def parameter_wrapper(field_name=None):
        def wrapper(func):
            field = CalculatedField(func, field_name)
            _handlers.append(field)
            return field
        return wrapper
    return parameter_wrapper


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add="True")
    modified_at = models.DateTimeField(auto_now="True")

    class Meta:
        abstract = True

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    @classmethod
    def get_admin_serializer(cls):
        if hasattr(cls, 'SearchProvider'):
            path = cls.SearchProvider.admin_serializer.split('.')
            module = ".".join(path[:-1])
            module_cls = path[-1]
            mod = importlib.import_module(module)
            s = getattr(mod, module_cls)
            return s

        else:
            mod = importlib.import_module('cotidia.admin.serializers')

            class GenericSerializer(mod.AdminModelSerializer):
                class Meta:
                    model = cls
                    fields = '__all__'

            return GenericSerializer
