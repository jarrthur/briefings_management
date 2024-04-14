from django.contrib import admin

from core.models import Briefing, Category, Retailer, Vendor

# Register your models here.
admin.site.register(Briefing)
admin.site.register(Category)
admin.site.register(Retailer)
admin.site.register(Vendor)
