from django.urls import path
from core.views import *


urlpatterns = [
    path('', BaseListView.as_view(), name = 'base-view'),
    path('<str:category_slug>', CategoryDetailView.as_view(), name = 'category-detail'),
    path('<str:category_slug>/<str:product_slug>', ProductDetailView.as_view(), name = 'product-detail'),
]