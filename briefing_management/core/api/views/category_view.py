from rest_framework import viewsets

from core.api.serializers import CategorySerializer
from core.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = [
        "get",
        "post",
        "put",
    ]
    lookup_field = "id"
