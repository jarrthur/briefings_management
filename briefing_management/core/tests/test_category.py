from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import MagicMock

from django.test import TestCase
from django.urls import reverse

from core.api.serializers import CategorySerializer
from core.models import Category


class TestCategoryModel(TestCase):

    def test_create_initial_all_categories_and_exists(self):
        Category.create_initial_categories()

        for category in Category.INITIAL_CATEGORIES:
            self.assertTrue(Category.objects.filter(name=category).exists())

    def test_create_initial_categories_mock(self):
        Category.objects.get_or_create = MagicMock()

        Category.create_initial_categories()

        Category.objects.get_or_create.assert_any_call(name="Novo Produto")
        Category.objects.get_or_create.assert_any_call(name="Troca de Fornecedor")
        Category.objects.get_or_create.assert_any_call(name="Reformulação de Produto")


class TestCategoryApiView(APITestCase):
    # TODO: Create tests for Category Serializer separately

    def create_category(
        self, name: str = "Novo Produto", description: str = "Descrição do Produto"
    ):
        return Category.objects.create(name=name, description=description)

    def create_initial_categories(self):
        Category.create_initial_categories()

    def get_category_data(self):
        return {"name": "Novo Produto", "description": "Descrição do Produto"}

    def test_data_category_is_valid(self):
        data = self.get_category_data()
        category_serializer = CategorySerializer(data=data)

        self.assertTrue(category_serializer.is_valid())

    def test_list_categories_and_check_initial(self):
        self.create_initial_categories()

        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        response = self.client.get(reverse("core:category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), category_serializer.data)

    def test_create_category(self):
        category_data = self.get_category_data()
        category_serializer = CategorySerializer(data=category_data)

        self.assertTrue(category_serializer.is_valid())

        response = self.client.post(
            reverse("core:category-create"),
            data=category_serializer.data,
        )

        self.assertTrue(Category.objects.filter(**category_data).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json().get("name"), category_serializer.data.get("name")
        )

    def test_retrieve_category(self):
        category = self.create_category()
        category_serializer = CategorySerializer(category)

        response = self.client.get(reverse("core:category-detail", args=[category.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, category_serializer.data)

    def test_update_category(self):
        category = self.create_category()
        new_category_name = "Novo Produto 2"
        new_data = {"name": new_category_name, "description": "Descrição do Produto"}
        category_serializer = CategorySerializer(category, data=new_data)

        response = self.client.put(
            reverse("core:category-detail", args=[category.id]), data=new_data
        )
        self.assertTrue(category_serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("name"), new_category_name)
        self.assertTrue(Category.objects.filter(name=new_category_name).exists())

    def test_delete_category_method_no_allowed(self):
        """Test if delete method is not allowed and category still exists"""
        category = self.create_category()
        response = self.client.delete(
            reverse("core:category-detail", args=[category.id])
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Category.objects.filter(id=category.id).exists())
