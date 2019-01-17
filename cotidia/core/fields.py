import logging

from django.utils.module_loading import import_string
from django.db.models.fields.files import FieldFile, FileField

from cotidia.file.conf import settings

logger = logging.getLogger(__name__)


class PublicFieldFile(FieldFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(settings, "PUBLIC_FILE_STORAGE"):
            self.storage = import_string(settings.PUBLIC_FILE_STORAGE)()
        else:
            logger.warning("PUBLIC_FILE_STORAGE not set.")


class PublicFileField(FileField):
    attr_class = PublicFieldFile


class CalculatedField:
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
