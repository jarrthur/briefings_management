from rest_framework import status
from rest_framework.test import APITestCase

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


from core.api.serializers import BriefingSerializer
from core.models import Retailer, Vendor, Category, Briefing


class BaseBriefingTestMixin:
    @classmethod
    def create_briefing(cls, name: str = "New Briefing") -> Briefing:
        return Briefing.objects.create(
            name=name,
            retailer=cls.retailer,
            responsible=cls.vendor,
            category=cls.category,
            release_date=timezone.now().date(),
            available=10,
        )

    @classmethod
    def setUpTestData(cls) -> None:
        cls.retailer: Retailer = Retailer.objects.create(name="Test Retailer")
        cls.vendor: Vendor = Vendor.objects.create(name="Test Vendor")
        cls.category: Category = Category.objects.create(name="Test Category")


class BriefingModelTests(BaseBriefingTestMixin, TestCase):

    def test_create_briefing(self):
        briefing = self.create_briefing()
        self.assertEqual(briefing.name, "New Briefing")
        self.assertEqual(briefing.retailer, self.retailer)
        self.assertEqual(briefing.responsible, self.vendor)
        self.assertEqual(briefing.category, self.category)
        self.assertEqual(briefing.release_date, timezone.now().date())
        self.assertEqual(briefing.available, 10)

    def test_briefing_str(self):
        name = "Briefing String Representation"
        briefing = self.create_briefing(name=name)
        self.assertEqual(str(briefing), name)

    def test_cascade_delete_retailer(self):
        self.create_briefing(name="Cascading Briefing")
        self.retailer.delete()
        with self.assertRaises(Briefing.DoesNotExist):
            Briefing.objects.get(name="Cascading Briefing")


class TestBriefingSerializer(BaseBriefingTestMixin, TestCase):
    DEFAULT_BRIEFING_NAME = "New Briefing"

    def get_briefing_data(self):
        return {
            "name": self.DEFAULT_BRIEFING_NAME,
            "retailer": self.retailer.id,
            "responsible": self.vendor.id,
            "category": self.category.id,
            "release_date": timezone.now().date(),
            "available": 10,
        }

    def test_data_briefing_is_valid(self):
        data = self.get_briefing_data()
        briefing_serializer = BriefingSerializer(data=data)

        self.assertTrue(briefing_serializer.is_valid())

    def test_create_briefing(self):
        briefing_data = self.get_briefing_data()
        briefing_serializer = BriefingSerializer(data=briefing_data)

        self.assertTrue(briefing_serializer.is_valid())
        self.assertEqual(briefing_serializer.save().name, self.DEFAULT_BRIEFING_NAME)
        self.assertTrue(
            Briefing.objects.filter(name=self.DEFAULT_BRIEFING_NAME).exists()
        )


class TestBriefingListApiView(BaseBriefingTestMixin, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("core:briefings-list")

    def test_list_briefings(self):
        self.create_briefing()
        self.create_briefing()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data[0]["name"], Briefing.objects.first().name
        )

    def test_list_briefings_serializer_data(self):
        serializer_data = BriefingSerializer(
            [self.create_briefing(), self.create_briefing()], many=True
        ).data
        response = self.client.get(self.url)

        self.assertEqual(response.data, serializer_data)

class TestBriefingCreateApiView(BaseBriefingTestMixin, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("core:briefing-create")
        cls.valid_payload = {
            "name": "New Briefing",
            "retailer": cls.retailer.id,
            "responsible": cls.vendor.id,
            "category": cls.category.id,
            "release_date": timezone.now().date(),
            "available": 10,
        }

    def test_create_briefing(self):
        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Briefing.objects.count(), 1)
        self.assertEqual(response.data["name"], self.valid_payload["name"])

    def test_create_briefing_invalid_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["name"] = ""
        response = self.client.post(self.url, data=invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Briefing.objects.count(), 0)

    
class TestBriefingDetailUpdateApiView(BaseBriefingTestMixin, APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.briefing = cls.create_briefing()
        cls.url = reverse("core:briefing-detail", args=[cls.briefing.id])
        cls.valid_payload = {
            "name": "Updated Briefing",
            "retailer": cls.retailer.id,
            "responsible": cls.vendor.id,
            "category": cls.category.id,
            "release_date": timezone.now().date(),
            "available": 10,
        }

    def test_retrieve_briefing(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.briefing.name)

    def test_update_briefing(self):
        response = self.client.put(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.briefing.refresh_from_db(fields=["name"])
        self.assertEqual(self.briefing.name, self.valid_payload["name"])
        self.assertEqual(response.data["name"], self.valid_payload["name"])

    def test_update_briefing_invalid_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["name"] = ""
        response = self.client.put(self.url, data=invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.briefing.name, invalid_payload["name"])