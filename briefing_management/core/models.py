from django.db import models


# TODO: Check if BigAutoField is more appropriate for id fields, because OpenAPI uses int64
class Briefing(models.Model):
    name = models.CharField(max_length=100)
    retailer = models.ForeignKey(
        "Retailer", on_delete=models.CASCADE, verbose_name="Retailer"
    )
    responsible = models.ForeignKey(
        "Vendor", on_delete=models.CASCADE, verbose_name="Responsible"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Category"
    )
    release_date = models.DateField()
    available = models.IntegerField()  # TODO: Check if BooleanField is more appropriate

    def __str__(self) -> str:
        return self.name


class Retailer(models.Model):
    name = models.CharField(max_length=100)
    vendors = models.ManyToManyField("Vendor", verbose_name="Vendors")

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
        for category in cls.INITIAL_CATEGORIES:
            cls.objects.get_or_create(name=category)
