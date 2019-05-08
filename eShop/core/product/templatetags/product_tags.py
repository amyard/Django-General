from django import template
from django.db.models import Count, Case, When
from ..models import Product, Like, Comment


register = template.Library()


@register.simple_tag
def show_latest_product(count=10):
    return Product.objects.order_by('-id')[:count]


@register.simple_tag
def most_liked_products(count=12):
    uniq_ids = Like.objects.values('product').annotate(count=Count('product')).order_by('-count')[:count].values_list('product', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(uniq_ids)])
    res = Product.objects.filter(id__in=uniq_ids).order_by(preserved)
    return res

@register.simple_tag
def most_commented_products(count=12):
    uniq_ids = Comment.objects.values('product').annotate(count=Count('product')).order_by('-count')[:count].values_list('product', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(uniq_ids)])
    res = Product.objects.filter(id__in=uniq_ids).order_by(preserved)
    return res