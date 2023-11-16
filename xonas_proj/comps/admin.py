from django.contrib import admin
from .models import Category, Sku
# Register your models here.

class SkuAdmin(admin.ModelAdmin):
    list_display = (
        'category',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'min_price',
        'max_price',
        'min_sells',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Sku, SkuAdmin)