from django.test import TestCase

from cotidia.account import fixtures
from cotidia.core.models import Status
from cotidia.core.tests.models import GenericItem


class StatusModelTest(TestCase):
    @fixtures.superuser
    def setUp(self):
        self.item = GenericItem.objects.create()
        self.kwargs = {
            "status": "SENT",
            "notes": "Sent with Cotidia Mail",
            "taxonomy": "status",
            "user": self.superuser,
            "content_object": self.item,
        }

    def test_create(self):
        status = Status.objects.create(**self.kwargs)
        status.refresh_from_db()
        self.assertEqual(status.status, "SENT")
        self.assertEqual(status.notes, "Sent with Cotidia Mail")
        self.assertEqual(status.taxonomy, "status")
        self.assertEqual(status.user, self.superuser)
        self.assertEqual(status.content_object, self.item)
        self.assertTrue(status.created_at)

    def test_author_user(self):
        status = Status.objects.create(**self.kwargs)
        status.refresh_from_db()
        self.assertEqual(status.author, self.superuser)

    def test_author_auto(self):
        kwargs = self.kwargs.copy()
        del kwargs["user"]
        status = Status.objects.create(**kwargs)
        status.refresh_from_db()
        self.assertEqual(status.author, "AUTO")

    def test_order_by(self):
        """Order by date DESC"""
        status_1 = Status.objects.create(**self.kwargs)
        status_2 = Status.objects.create(**self.kwargs)
        statuses = Status.objects.all()
        self.assertEqual(statuses[0], status_2)
        self.assertEqual(statuses[1], status_1)

    def test_to_string(self):
        """To string should be in the form of:

        <app_label>.<model_name> <status> <created_at> <user/AUTO>
        """
        status = Status.objects.create(**self.kwargs)
        self.assertEqual(
            str(status),
            "tests.genericitem SENT {} {}".format(
                status.created_at.strftime("%Y-%m-%d %H:%M"), self.superuser
            ),
        )
        pass


class StatusModelMixinTest(TestCase):
    @fixtures.superuser
    def setUp(self):
        self.item = GenericItem.objects.create()
        self.other_item = GenericItem.objects.create()

    def get_item_status(self):
        return Status.objects.filter(
            content_type=self.item.content_type, object_id=self.item.id
        ).first()

    def test_status_set_user(self):
        self.item.status_set("SENT", user=self.superuser, taxonomy="status")
        status = self.get_item_status()
        item = GenericItem.objects.get(id=self.item.id)
        self.assertEqual(item.status, "SENT")
        self.assertEqual(status.status, "SENT")
        self.assertEqual(status.author, self.superuser)

    def test_status_set_auto(self):
        self.item.status_set("SENT", taxonomy="status")
        status = self.get_item_status()
        item = GenericItem.objects.get(id=self.item.id)
        self.assertEqual(item.status, "SENT")
        self.assertEqual(status.status, "SENT")
        self.assertEqual(status.author, "AUTO")

    def test_status_set_taxonomy(self):
        self.item.status_set("SENT", taxonomy="mail", user=self.superuser)
        status = self.get_item_status()
        self.assertEqual(status.taxonomy, "mail")

    def test_status_set_notes(self):
        self.item.status_set(
            "SENT", notes="Test status", user=self.superuser, taxonomy="status"
        )
        status = self.get_item_status()
        self.assertEqual(status.notes, "Test status")

    def test_status_list(self):
        status_1 = self.item.status_set("DRAFT", user=self.superuser, taxonomy="status")
        status_2 = self.item.status_set("SENT", user=self.superuser, taxonomy="status")
        self.assertEqual(self.item.status_list().count(), 2)
        self.assertEqual(self.item.status_list()[0], status_2)
        self.assertEqual(self.item.status_list()[1], status_1)

    def test_status_latest(self):
        self.item.status_set("DRAFT", user=self.superuser, taxonomy="status")
        status_2 = self.item.status_set("SENT", user=self.superuser, taxonomy="status")
        self.assertEqual(self.item.status_latest(), status_2)

    def test_status_list_taxonomy(self):
        """Filter by taxonomy"""
        status_1 = self.item.status_set("DRAFT", taxonomy="status")
        status_2 = self.item.status_set("SENT", taxonomy="payment_status")
        self.assertEqual(self.item.status_list(taxonomy="status").count(), 1)
        self.assertEqual(self.item.status_list(taxonomy="status")[0], status_1)
        self.assertEqual(self.item.status_list(taxonomy="payment_status").count(), 1)
        self.assertEqual(self.item.status_list(taxonomy="payment_status")[0], status_2)
        item = GenericItem.objects.get(id=self.item.id)
        self.assertEqual(item.status, "DRAFT")
        self.assertEqual(item.payment_status, "SENT")

    def test_status_latest_taxonomy(self):
        """Latest by taxonomy"""
        status_1 = self.item.status_set("DRAFT", taxonomy="status")
        status_2 = self.item.status_set("SENT", taxonomy="payment_status")
        self.assertEqual(self.item.status_latest(taxonomy="status"), status_1)
        self.assertEqual(self.item.status_latest(taxonomy="payment_status"), status_2)

    def test_status_list_item_only(self):
        """Ensure statuses are for the item only"""
        status_1 = self.item.status_set("DRAFT", taxonomy="status")
        status_2 = self.other_item.status_set("DRAFT", taxonomy="status")
        self.assertEqual(self.item.status_list().count(), 1)
        self.assertEqual(self.item.status_list()[0], status_1)
        self.assertEqual(self.other_item.status_list().count(), 1)
        self.assertEqual(self.other_item.status_list()[0], status_2)
