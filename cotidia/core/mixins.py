from django.db import models
from django.db.models import OuterRef, Subquery
from django.contrib.contenttypes.models import ContentType

from cotidia.core.models import Status


class StatusManager(models.Manager):
    def get_queryset(self):
        if self.model.status_fields:
            content_type = ContentType.objects.get_for_model(self.model)
            q = {}
            for f in self.model.status_fields:
                statuses = Status.objects.filter(
                    content_type=content_type, object_id=OuterRef("pk"), taxonomy=f
                )
                q[f] = Subquery(statuses.values("status")[:1])
            return super().get_queryset().annotate(**q)
        else:
            return super().get_queryset()


class StatusModelMixin(models.Model):
    objects = StatusManager()

    class Meta:
        abstract = True

    def status_set(self, status, taxonomy, notes=None, user=None):
        kwargs = {
            "status": status,
            "notes": notes,
            "taxonomy": taxonomy,
            "user": user,
            "content_object": self,
        }
        return Status.objects.create(**kwargs)

    def status_list(self, taxonomy=None, user=None):
        queryset = Status.objects.filter(
            content_type=self.content_type, object_id=self.id
        )
        if taxonomy:
            queryset = queryset.filter(taxonomy=taxonomy)
        if user:
            if user == "AUTO":
                queryset = queryset.filter(user=None)
            else:
                queryset = queryset.filter(user=user)
        return queryset

    def status_latest(self, taxonomy=None, user=None):
        return self.status_list(taxonomy=taxonomy).first()
