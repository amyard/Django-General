from django.views.generic.list import MultipleObjectMixin
from django.db.models import Count
from core.models import Category


class SideBarMixin(MultipleObjectMixin):

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all().order_by('name')
        context['count_products'] = Category.objects.all().annotate(count = Count('products__title')).values('name', 'count')

        return context