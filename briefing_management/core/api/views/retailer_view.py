from rest_framework import generics

from core.models import Retailer
from core.api.serializers import RetailerSerializer


class BaseRetailerApiViewMixin:
    serializer_class = RetailerSerializer

    def get_queryset(self):
        return Retailer.objects.all().prefetch_related("vendors")


class RetailerListApiView(
    BaseRetailerApiViewMixin,
    generics.ListAPIView,
): ...


class RetailerCreateApiView(
    BaseRetailerApiViewMixin,
    generics.CreateAPIView,
): ...


class RetailerDetailUpdateApiView(
    BaseRetailerApiViewMixin,
    generics.RetrieveUpdateAPIView,
):
    lookup_field = "id"
    http_method_names = ["get", "put"]
