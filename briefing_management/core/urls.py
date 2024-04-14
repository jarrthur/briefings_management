from django.urls import path

from core.api.views.briefing_view import (
    BriefingDetailUpdateApiView,
    BriefingListApiView,
    BriefingCreateApiView,
)
from core.api.views.retailer_view import (
    RetailerDetailUpdateApiView,
    RetailerListApiView,
    RetailerCreateApiView,
)

app_name = "core"

urlpatterns = [
    # Briefing
    path("briefings/", BriefingListApiView.as_view(), name="briefings-list"),
    path(
        "briefing/<int:id>/",
        BriefingDetailUpdateApiView.as_view(),
        name="briefing-detail",
    ),
    path("briefing/", BriefingCreateApiView.as_view(), name="briefing-create"),
    # Retailer
    path("retailers/", RetailerListApiView.as_view(), name="retailers-list"),
    path("retailer/<int:id>/", RetailerDetailUpdateApiView.as_view(), name="retailer-detail"),
    path("retailer/", RetailerCreateApiView.as_view(), name="retailer-create"),
]
