from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q

from product.models import Category, Brand, Product, Like, Comment
from product.mixins import SideBarMixin
from product.forms import LikeForm, CommentForm
from cart.forms import CartAddProductForm
from product.utils import get_ip_from_request

import datetime


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



class ProductDetailView(SideBarMixin, DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    form = CartAddProductForm

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['product'] = self.get_object()
        context['cart_product_form'] = self.form
        context['comment_form'] = CommentForm()

        if self.request.user.username == '':
            try:
                ip = self.request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
            except:
                ip = self.request.META.get('REMOTE_ADDR')
            context['buttons'] = Like.objects.filter(product=self.get_object(), ip = ip)
        else:
            context['buttons'] = Like.objects.filter(product=self.get_object(), user = self.request.user)

        return context



class LikeToggleView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.request.GET.get('product_id')
        product = Product.objects.get(id=product_id)

        if self.request.user.is_anonymous:
            likes = Like.objects.filter(product=product).values_list('ip', flat=True)
            ip = get_ip_from_request(request)
            if ip not in likes:
                Like.objects.create(product=product, ip=ip)
                message_tag='success'
                message_text='Вы посталиви Лайк продукту.'
                button = ['Dislike', 'danger']
            else:
                Like.objects.filter(product=product, ip=ip).delete()
                message_tag = 'danger'
                message_text = 'Вам не понравился продукт.'
                button = ['Like', 'success']

        elif self.request.user.is_authenticated:
            likes = Like.objects.filter(product=product).values_list('user', flat=True)
            if self.request.user.id not in likes:
                Like.objects.create(product=product, user=self.request.user)
                message_tag = 'success'
                message_text = 'Вы посталиви Лайк продукту.'
                button = ['Dislike', 'danger']
            else:
                Like.objects.filter(product=product, user=self.request.user).delete()
                message_tag = 'danger'
                message_text = 'Вам не понравился продукт.'
                button = ['Like', 'success']

        res = Like.objects.filter(product=product).count()

        data = {
            'res':res,
            'message_tag':message_tag,
            'message_text':message_text,
            'button':button
        }
        return JsonResponse(data)



class CreateCommentView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        comment = self.request.POST.get('comment')

        if comment == '':
            return JsonResponse({}, safe=False)
        else:
            if self.request.user.is_authenticated:
                new_comment = Comment.objects.create(product=Product.objects.get(id=product_id), user=request.user, text=comment)
            else:
                new_comment = Comment.objects.create(product=Product.objects.get(id=product_id), ip=get_ip_from_request(request), text=comment)

            created = new_comment.created.strftime('%b %d, %Y, %I:%M %p').replace('PM', 'p.m.').replace('AM', 'a.m.')
            comment = [{'text': new_comment.text,
                        'created': created}]
            return JsonResponse(comment, safe=False)