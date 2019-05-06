from django.contrib import admin
from .models import Category, Brand, Product, Like, Comment
from tinymce.widgets import TinyMCE
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
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
    formfield_overrides = {
        models.TextField: {'widget':TinyMCE()}
    }


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip',)
    search_fields = ['product']

    fieldsets = [
        ('Product name', {'fields':['product']}),
        ('User Info', {'fields': ['user', 'ip']})
    ]



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ip',)
    search_fields = ['product']

    fieldsets = [
        ('Product name', {'fields': ['product']}),
        ('User Info', {'fields': ['user', 'ip']}),
        ('Content', {'fields': ['text']})
    ]