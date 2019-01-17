from django.db import models

from cotidia.core.models import Status


class StatusModelMixin(models.Model):
    status = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True

    def status_set(self, status, notes=None, taxonomy=None, user=None):
        self.status = status
        self.save()
        print("save status", self.status)
        kwargs = {
            "status": status,
            "notes": notes,
            "taxonomy": taxonomy,
            "user": user,
            "content_object": self,
        }
        return Status.objects.create(**kwargs)

    def status_list(self, taxonomy=None):
        queryset = Status.objects.filter(
            content_type=self.content_type, object_id=self.id
        )
        if taxonomy:
            queryset = queryset.filter(taxonomy=taxonomy)
        return queryset

    def status_latest(self, taxonomy=None):
        return self.status_list(taxonomy=taxonomy).first()
