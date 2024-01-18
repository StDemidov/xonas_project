from django.contrib import admin
from .models import Category, ExcBrands, ExcNaming, Sku

class SkuAdmin(admin.ModelAdmin):
    list_display = (
        'sku_id',
        'created_at',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'min_price',
        'max_price',
        'min_sells',
        'fix_avg_sells',
        'min_total_sells'
    )
    list_editable = (
        'min_price',
        'max_price',
        'min_sells',
        'fix_avg_sells',
        'min_total_sells'
    )


class ExcBrandsAdmin(admin.ModelAdmin):
    list_display = ('brand',)


class ExcNamingAdmin(admin.ModelAdmin):
    list_display = ('word',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(ExcBrands, ExcBrandsAdmin)
admin.site.register(ExcNaming, ExcNamingAdmin)
admin.site.register(Sku, SkuAdmin)
