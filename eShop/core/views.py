from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.core.paginator import Paginator


from .models import Category, Brand, Product
from core.mixins import SideBarMixin




class BaseListView(SideBarMixin, ListView):
    template_name = 'core/main.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data(*args, **kwargs)
        context['products'] = Product.objects.all().order_by('?')[:9]
        context['slider_products'] = Product.objects.all().order_by('?')[:5]
        return context



class CategoryDetailView(SideBarMixin, DetailView):
    template_name = 'core/category-detail.html'
    model = Category
    # context_object_name = 'category'
    slug_url_kwarg = 'category_slug'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['category'] = self.get_object()

        category_slug = self.kwargs['category_slug']
        p = Paginator(Product.objects.filter(category__slug=category_slug), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context['products'] = p.get_page(page_number)
        return context



class ProductDetailView(SideBarMixin, DetailView):
    template_name = 'core/product-detail.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['product'] = self.get_object

        return context
