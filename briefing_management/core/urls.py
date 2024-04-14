from django.urls import path

from core.api.views.briefing_view import (
    BriefingDetailUpdateApiView,
    BriefingListApiView,
    BriefingCreateApiView,
)
from core.api.views.category_view import CategoryViewSet
from core.api.views.retailer_view import (
    RetailerDetailUpdateApiView,
    RetailerListApiView,
    RetailerCreateApiView,
)
from core.api.views.vendor_view import VendorViewSet

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
    path(
        "retailer/<int:id>/",
        RetailerDetailUpdateApiView.as_view(),
        name="retailer-detail",
    ),
    path("retailer/", RetailerCreateApiView.as_view(), name="retailer-create"),
]

# Urls coming from ModelViewSet, seeking greater generalization in simpler models
urlpatterns += [
    # Vendor
    path("vendors/", VendorViewSet.as_view({"get": "list"}), name="vendor-list"),
    path("vendor/", VendorViewSet.as_view({"post": "create"}), name="vendor-create"),
    path(
        "vendor/<int:id>/",
        VendorViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="vendor-detail",
    ),
    # Category
    path("categories/", CategoryViewSet.as_view({"get": "list"}), name="category-list"),
    path(
        "category/", CategoryViewSet.as_view({"post": "create"}), name="category-create"
    ),
    path(
        "category/<int:id>/",
        CategoryViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="category-detail",
    ),
]
