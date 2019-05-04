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

        context['brands'] = Product.objects.filter(category__slug=category_slug).values('brand__name', 'brand__slug').distinct().order_by().annotate(count=Count('title'))
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




class BrandDetailView(SideBarMixin, ListView):
    template_name = 'product/category-detail.html'
    model = Brand
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(BrandDetailView, self).get_context_data(*args, **kwargs)


        category_slug = self.kwargs['category_slug']
        brand_slug = self.kwargs['brand_slug']

        p = Paginator(Product.objects.filter(category__slug=category_slug, brand__slug=brand_slug), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context['products'] = p.get_page(page_number)

        context['brand_view'] = True
        context['brand_test'] = Product.objects.filter(category__slug=category_slug, brand__slug=brand_slug)[0]
        return context
