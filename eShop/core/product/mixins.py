from django.views.generic.list import MultipleObjectMixin
from django.db.models import Count
from django.core.paginator import Paginator

from core.product.forms import FilterProduct
from core.product.models import Category


class SideBarMixin(MultipleObjectMixin):

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all().order_by('name')
        context['count_products'] = Category.objects.all().annotate(count = Count('products__title')).values('name', 'count')

        return context



class ProductBrandDetailMixin(MultipleObjectMixin):
    template_name = 'product/category-detail.html'
    model = None
    paginate_by = 8
    form_class = FilterProduct


    def get_context_data(self, *args, **kwargs):
        context = {}

        p = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context['products'] = p.get_page(page_number)

        context['form'] = FilterProduct()
        return context