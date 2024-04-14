from django.db import models
from django.utils.translation import gettext_lazy as _


class Briefing(models.Model):
    name = models.CharField(max_length=100)
    retailer = models.ForeignKey(
        "Retailer", on_delete=models.CASCADE, verbose_name=_("Retailer")
    )
    responsible = models.ForeignKey(
        "Vendor", on_delete=models.CASCADE, verbose_name=_("Responsible")
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name=_("Category")
    )
    release_date = models.DateField()
    # TODO: Check if BooleanField is more appropriate for available field
    available = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Retailer(models.Model):
    name = models.CharField(max_length=100)
    vendors = models.ManyToManyField("Vendor", verbose_name=_("Vendors"))

    def __str__(self) -> str:
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    INITIAL_CATEGORIES = [
        "Novo Produto",
        "Troca de Fornecedor",
        "Reformulação de Produto",
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create_initial_categories(cls) -> None:
        for category_name in cls.INITIAL_CATEGORIES:
            cls.objects.get_or_create(name=category_name)
