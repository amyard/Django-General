from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, Count

from core.product.models import Category, Brand, Product, Like, Comment
from core.product.mixins import SideBarMixin, ProductBrandDetailMixin
from core.product.forms import LikeForm, CommentForm, CommentFormModal, FilterProduct
from core.cart.forms import CartAddProductForm
from core.product.utils import get_ip_from_request

import datetime
from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalDeleteView



class BaseListView(SideBarMixin, ListView):
    template_name = 'product/main.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data(*args, **kwargs)
        context['slider_products'] = Product.objects.all().order_by('?')[:5]
        return context



class CategoryDetailView(ProductBrandDetailMixin, ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        context['category'] = self.model.objects.get(slug=self.kwargs['category_slug'])
        context['brands'] = self.get_queryset().values('brand__name', 'brand__slug').distinct().order_by().annotate(count=Count('title'))
        return context



class BrandDetailView(ProductBrandDetailMixin, ListView):
    model = Brand

    def get_context_data(self, *args, **kwargs):
        context = super(BrandDetailView, self).get_context_data(*args, **kwargs)

        # исп один html_template для бренда и категорий.
        # Если True - добвляет Brand к  Home > Сategory > Brand
        context['brand_view'] = True

        # display in block title - Brand name
        context['brand_test'] = Product.objects.filter(category__slug=self.kwargs['category_slug'], brand__slug=self.kwargs['brand_slug'])[0]
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

        # при загрузки страници отображает кнопки Like/Dislike в правильном цвете
        if self.request.user.username == '':
            try:
                ip = self.request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
            except:
                ip = self.request.META.get('REMOTE_ADDR')
            context['buttons'] = Like.objects.filter(product=self.get_object(), ip = ip)

            # отображаем кнопки Delete/Edit для комментариев - только ip
            context['ip'] = ip
        else:
            context['buttons'] = Like.objects.filter(product=self.get_object(), user = self.request.user)

            # отображаем кнопки Delete/Edit для комментариев - только user
            context['user'] = self.request.user


        return context



class LikeToggleView(View):

    def get(self, request, *args, **kwargs):
        product_id = self.request.GET.get('product_id')
        product = Product.objects.get(id=product_id)

        if self.request.user.is_anonymous:
            if not Like.objects.filter(product=product, ip=get_ip_from_request(request)).exists():
                Like.objects.create(product=product, ip=get_ip_from_request(request))
                # для JQuery ниже
                message_tag='success'
                message_text='Вы посталиви Лайк продукту.'
                button = ['Dislike', 'danger']
            else:
                Like.objects.filter(product=product, ip=get_ip_from_request(request)).delete()
                # для JQuery ниже
                message_tag = 'danger'
                message_text = 'Вам не понравился продукт.'
                button = ['Like', 'success']

        elif self.request.user.is_authenticated:
            if not Like.objects.filter(product=product, user = self.request.user).exists():
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
            count = Comment.objects.filter(product=Product.objects.get(id=product_id)).count()
            comment = [{'text': new_comment.text,
                        'created': created,
                        'count': count,
                        'ids':new_comment.id}]
            return JsonResponse(comment, safe=False)



class CommentDeleteView(BSModalDeleteView):
    model = Comment
    template_name = 'product/actions/comment-delete.html'
    success_message = 'Комментарий был удален.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')



class CommentUpdateView(BSModalUpdateView):
    model = Comment
    form_class = CommentFormModal
    template_name = 'product/actions/comment-update.html'
    success_message = 'Комментарий был обновлен.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')