from django.db import models

from cotidia.core.models import Status


class StatusModelMixin:
    status = models.CharField(max_length=255, null=True)

    def status_set(self, status, notes=None, taxonomy=None, user=None):
        self.status = status
        self.save()
        kwargs = {
            "status": status,
            "notes": notes,
            "taxonomy": taxonomy,
            "user": user,
            "content_object": self,
        }
        return Status.objects.create(**kwargs)

    def status_list(self, taxonomy=None):
        return Status.objects.filter(
            content_type=self.content_type, object_id=self.id, taxonomy=taxonomy
        )

    def status_latest(self, taxonomy=None):
        return self.status_list(taxonomy=taxonomy).first()
