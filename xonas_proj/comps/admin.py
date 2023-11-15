from django.contrib import admin
from .models import Category, Sku
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'min_price',
        'max_price',
        'min_sells',
    )

admin.site.register(Category, CategoryAdmin)