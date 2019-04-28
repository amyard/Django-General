from django.contrib import admin
from .models import Category, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'brand', 'title','price')
    list_filter = ['category', 'brand', 'available']
    prepopulated_fields = {'slug':('title',)}

    fieldsets = [
        ('Title/slug', {'fields': ['title', 'slug']}),
        ('General Info', {'fields': ['category', 'brand', 'price']}),
        ('Content', {'fields': ['description', 'image']}),
        ('Available', {'fields': ['available']})
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)

