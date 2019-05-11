from django.views.generic.list import MultipleObjectMixin
from django.db.models import Count
from django.core.paginator import Paginator

from core.product.forms import FilterProduct
from core.product.models import Category, Comment, Like, Product


class SideBarMixin(MultipleObjectMixin):

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['categories'] = Category.objects.all().order_by('name')
        context['count_products'] = Category.objects.all().annotate(count = Count('products__title')).values('name', 'count')

        return context


#  Не учитывает в фильтрации Бренды. Сбрасывает настройки фильтрации
# TODO - созранять значения фильтрации в сессии и передавать во вьюху бренд
# TODO -  забить на геммор с сессиями. закинуть бренды как поле для фильтрации.
class ProductBrandDetailMixin(MultipleObjectMixin):
    template_name = 'product/category-detail.html'
    model = None
    paginate_by = 2
    form_class = FilterProduct


    def get_queryset(self, *args, **kwargs):
        qs = Product.objects.all()
        category_slug = self.kwargs['category_slug']
        brand_slug = self.kwargs.get('brand_slug', '')

        if category_slug: qs = qs.filter(category__slug=category_slug)
        if brand_slug: qs = qs.filter(brand__slug=brand_slug)

        # Фильтруем данные из формы
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        comments = self.request.GET.get('comments')
        likes = self.request.GET.get('likes')

        if price_from: qs = qs.filter(price__gte=price_from)
        if price_to: qs = qs.filter(price__lte=price_to)

        # TODO - 1 это "Все продукты" - пропускаем проверку
        # TODO - 2 это "Продукты без комментариев" / Продукты, которым не поставили "Like"
        # TODO - 3 это "Продукты с комментариями"  / Продукты, которым поставили "Like"
        product_with_comments = Comment.objects.values('product').annotate(count=Count('product')).order_by('-count').values_list('product', flat=True)
        if comments=='2':
            qs = qs.exclude(id__in=product_with_comments)
        elif comments=='3':
            qs = qs.filter(id__in=product_with_comments)

        product_with_likes = Like.objects.values('product').annotate(count=Count('product')).order_by('-count').values_list('product', flat=True)
        if likes == '2':
            qs = qs.exclude(id__in=product_with_likes)
        elif likes == '3':
            qs = qs.filter(id__in=product_with_likes)
        return qs


    def get_context_data(self, *args, **kwargs):
        context = {}

        p = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        context['products'] = p.get_page(page_number)

        context['form'] = self.form_class(
            initial={'price_from': self.request.GET.get('price_from'), 'price_to': self.request.GET.get('price_to'),
                     'comments': self.request.GET.get('comments'), 'likes': self.request.GET.get('likes')})

        # можно исп {% if 'price_from' in request.get_full_path %} заместь всего ниже.
        # исп файл pagg-fill из папки 'not use'
        # минус - при нажатии повторно на одну и ту же страницу - дублирует page=<номер страницы> в url
        if self.request.GET.get('price_from') or self.request.GET.get('price_to') or self.request.GET.get('comments') or self.request.GET.get('likes'):
            context['filter_cond'] = f"?price_from={self.request.GET.get('price_from')}&price_to={self.request.GET.get('price_to')}&comments={self.request.GET.get('comments')}&likes={self.request.GET.get('likes')}"

        return context