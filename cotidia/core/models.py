import uuid
import importlib

from django.db import models
from django.urls import reverse, NoReverseMatch
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add="True")
    modified_at = models.DateTimeField(auto_now="True")

    class Meta:
        abstract = True

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_parent_field(self):
        if hasattr(self, "parent_field"):
            return self.parent_field
        else:
            return None

    def get_parent(self):
        if self.get_parent_field():
            return getattr(self, self.get_parent_field())
        else:
            return None

    def get_url_kwargs(self):
        kwargs = {"pk": self.id}
        parent = self.get_parent()
        if parent:
            kwargs.update({"parent_id": parent.id})
        return kwargs

    def get_admin_detail_url(self):
        try:
            return reverse(
                "{app_label}-admin:{model_name}-detail".format(
                    app_label=self._meta.app_label, model_name=self._meta.model_name
                ),
                kwargs=self.get_url_kwargs(),
            )
        except NoReverseMatch:
            return "no-reverse-match"

    def get_admin_update_url(self):
        try:
            return reverse(
                "{app_label}-admin:{model_name}-update".format(
                    app_label=self._meta.app_label, model_name=self._meta.model_name
                ),
                kwargs=self.get_url_kwargs(),
            )
        except NoReverseMatch:
            return "no-reverse-match"

    def get_admin_delete_url(self):
        try:
            return reverse(
                "{app_label}-admin:{model_name}-delete".format(
                    app_label=self._meta.app_label, model_name=self._meta.model_name
                ),
                kwargs=self.get_url_kwargs(),
            )
        except NoReverseMatch:
            return "no-reverse-match"

    @classmethod
    def get_admin_serializer(cls):
        if hasattr(cls, "SearchProvider"):
            path = cls.SearchProvider.admin_serializer.split(".")
            module = ".".join(path[:-1])
            module_cls = path[-1]
            mod = importlib.import_module(module)
            s = getattr(mod, module_cls)
            return s

        else:
            mod = importlib.import_module("cotidia.admin.serializers")

            class GenericSerializer(mod.AdminModelSerializer):
                class Meta:
                    model = cls
                    fields = "__all__"

            return GenericSerializer


class BaseAddress(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    address_line_3 = models.CharField(max_length=255, null=True, blank=True)
    address_city = models.CharField(max_length=35)
    address_state = models.CharField(max_length=35, null=True, blank=True)
    address_postcode = models.CharField(max_length=8)
    address_country = models.CharField(max_length=2)

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    point = PointField(geography=True, dim=2, srid=4326, null=True)

    class Meta:
        abstract = True

    def address_to_string(self):
        address_fields = []
        if self.address_line_1:
            address_fields.append(self.address_line_1)
        if self.address_line_2:
            address_fields.append(self.address_line_2)
        if self.address_line_3:
            address_fields.append(self.address_line_3)
        if self.address_city:
            address_fields.append(self.address_city)
        if self.address_state:
            address_fields.append(self.address_state)
        if self.address_postcode:
            address_fields.append(self.address_postcode)
        if self.address_country:
            address_fields.append(self.address_country)

        return ", ".join(address_fields)

    def save(self, *args, **kwargs):
        if self.lng and self.lat:
            self.point = Point(self.lng, self.lat)
        super().save(*args, **kwargs)


class BaseStatus(BaseModel):
    status = models.CharField(max_length=255)
    taxonomy = models.CharField(max_length=255, null=True)
    notes = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def __str__(self):
        return "{}.{} {} {} {}".format(
            self.content_object._meta.app_label,
            self.content_object._meta.model_name,
            self.status,
            self.created_at.strftime("%Y-%m-%d %H:%M"),
            self.author,
        )

    @property
    def author(self):
        return self.user or "AUTO"


class Status(BaseStatus):
    pass
