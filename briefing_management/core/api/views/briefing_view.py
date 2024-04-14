from rest_framework import generics

from core.models import Briefing
from core.api.serializers import BriefingSerializer


class BaseBriefingApiViewMixin:
    queryset = (
        Briefing.objects.all()
    )  # Without select_related because an ID is returning as foreign key
    serializer_class = BriefingSerializer


class BriefingListApiView(BaseBriefingApiViewMixin, generics.ListAPIView): ...


class BriefingCreateApiView(BaseBriefingApiViewMixin, generics.CreateAPIView):
    pass


class BriefingDetailUpdateApiView(
    BaseBriefingApiViewMixin, generics.RetrieveUpdateAPIView
):
    http_method_names = ["get", "put"]
    lookup_field = "id"
