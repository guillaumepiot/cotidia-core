import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add="True")
    modified_at = models.DateTimeField(auto_now="True")

    class Meta:
        abstract = True

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)
