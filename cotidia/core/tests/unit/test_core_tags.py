from django.test import TestCase

from cotidia.account import fixtures
from cotidia.core.tests.models import GenericItem

from cotidia.core.templatetags.core_tags import status_list_for_obj


class StatusListForObjTest(TestCase):
    @fixtures.superuser
    @fixtures.admin_user
    def setUp(self):
        self.item = GenericItem.objects.create()

    def test_status_list_for_obj(self):
        self.item.status_set("DRAFT", user=self.superuser)
        self.item.status_set("DRAFT", user=self.superuser)

        queryset = status_list_for_obj(self.item)
        self.assertEqual(queryset.count(), 2)

    def test_status_list_for_obj_taxonomy(self):
        self.item.status_set("DRAFT")
        status_2 = self.item.status_set("DRAFT", taxonomy="mail")

        queryset = status_list_for_obj(self.item, taxonomy="mail")
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0], status_2)

    def test_status_list_for_obj_user(self):
        self.item.status_set("DRAFT", user=self.superuser)
        status_2 = self.item.status_set("DRAFT", user=self.admin_user)
        status_3 = self.item.status_set("DRAFT")

        queryset = status_list_for_obj(self.item, user=self.admin_user)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0], status_2)

        queryset = status_list_for_obj(self.item, user="AUTO")
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0], status_3)
