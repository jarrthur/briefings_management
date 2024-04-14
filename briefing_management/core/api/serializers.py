from base.serializers import BaseModelSerializer
from core.models import Briefing, Category, Retailer, Vendor


class BriefingSerializer(BaseModelSerializer):
    class Meta:
        model = Briefing
        fields = [
            "id",
            "name",
            "retailer",
            "responsible",
            "category",
            "release_date",
            "available",
        ]


class RetailerSerializer(BaseModelSerializer):
    class Meta:
        model = Retailer
        fields = [
            "id",
            "name",
            "vendors",
        ]


class VendorSerializer(BaseModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "name",
        ]


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
