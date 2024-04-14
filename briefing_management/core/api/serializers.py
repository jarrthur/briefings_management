from rest_framework import serializers

from core.models import Briefing, Category, Retailer, Vendor


class BriefingSerializer(serializers.ModelSerializer):
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


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = [
            "id",
            "name",
            "vendors",
        ]