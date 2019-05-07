from django.urls import path
from core.cart.views import *


app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartDeleteView.as_view(), name='cart_remove'),
]