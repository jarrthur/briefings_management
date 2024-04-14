from rest_framework import viewsets

from core.api.serializers import VendorSerializer
from core.models import Vendor


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    http_method_names = [
        "get",
        "post",
        "put",
    ]
    lookup_field = "id"