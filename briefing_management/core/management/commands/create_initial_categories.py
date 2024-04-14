from django.core.management.base import BaseCommand

from core.models import Category


class Command(BaseCommand):
    help = "Initializes the database with default category data."

    def handle(self, *args, **options):
        Category.create_initial_categories()
        self.stdout.write(self.style.SUCCESS("Successfully added default categories."))
