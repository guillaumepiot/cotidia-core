# import os
# import shutil

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission

# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission

# from cotidia.account.models import User
from cotidia.account import fixtures
from cotidia.core.tests.models import GenericItem

# from cotidia.file.models import File
# from cotidia.file.factory import FileFactory
# from cotidia.file.conf import settings


class StatusAdminTests(TestCase):
    @fixtures.superuser
    @fixtures.admin_user
    def setUp(self):
        self.item = GenericItem.objects.create()
        self.other_item = GenericItem.objects.create()

        self.status_1 = self.item.status_set("DRAFT")
        self.status_2 = self.item.status_set("READY", taxonomy="mail")
        self.other_item.status_set("DRAFT")
        self.other_item.status_set("CANCELLED")

        self.c = Client()

    def test_list_statuses_per_object(self):

        self.c.login(email=self.superuser.email, password=self.superuser_pwd)

        url = reverse(
            "generic-admin:status-history",
            kwargs={
                "app_label": self.item.content_type.app_label,
                "model": self.item.content_type.model,
                "object_id": self.item.id,
            },
        )

        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object_list"].count(), 2)
        self.assertEqual(response.context["object_list"][0], self.status_2)
        self.assertEqual(response.context["object_list"][1], self.status_1)

    def test_list_statuses_per_object_per_taxonomy(self):
        self.c.login(email=self.superuser.email, password=self.superuser_pwd)

        url = reverse(
            "generic-admin:status-history",
            kwargs={
                "app_label": self.item.content_type.app_label,
                "model": self.item.content_type.model,
                "object_id": self.item.id,
                "taxonomy": "mail",
            },
        )

        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object_list"].count(), 1)
        self.assertEqual(response.context["object_list"][0], self.status_2)

    def test_list_statuses_per_object_permission(self):
        self.c.login(email=self.admin_user.email, password=self.admin_user_pwd)

        url = reverse(
            "generic-admin:status-history",
            kwargs={
                "app_label": self.item.content_type.app_label,
                "model": self.item.content_type.model,
                "object_id": self.item.id,
                "taxonomy": "mail",
            },
        )

        response = self.c.get(url)
        self.assertEqual(response.status_code, 403)

        perm = Permission.objects.get(codename="change_genericitem")
        self.admin_user.user_permissions.add(perm)

        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
