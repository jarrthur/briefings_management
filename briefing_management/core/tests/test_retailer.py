from django.test import TestCase

from core.api.views.retailer_view import BaseRetailerApiViewMixin
from core.models import Retailer, Vendor


class TestBaseRetailerApiViewMixin(TestCase):

    def test_queryset(self):
        retailer = Retailer.objects.create(name="Test Retailer")
        vendor = Vendor.objects.create(name="Test Vendor")
        retailer.vendors.add(vendor)

        mixin = BaseRetailerApiViewMixin()

        self.assertIn(retailer, mixin.get_queryset())
        self.assertIn(vendor, retailer.vendors.all())
