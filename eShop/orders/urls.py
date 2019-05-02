from django.urls import path
from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name = 'order_create'),
    path('admin/order/<int:order_id>/', AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', AdminOrderPDFView.as_view(), name='admin_order_pdf'),
]

