from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.core.paginator import Paginator


from product.models import Category, Brand, Product
from product.mixins import SideBarMixin

from cart.forms import CartAddProductForm





class BaseListView(SideBarMixin, ListView):
    template_name = 'product/main.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data(*args, **kwargs)
        context['products'] = Product.objects.all().order_by('?')[:9]
        context['slider_products'] = Product.objects.all().order_by('?')[:5]
        return context



class CategoryDetailView(SideBarMixin, DetailView):
    template_name = 'product/category-detail.html'
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
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form = CartAddProductForm

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['product'] = self.get_object
        context['cart_product_form'] = self.form
        return context
