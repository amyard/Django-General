from django.urls import path
from core.product.views import *


app_name = 'product'

urlpatterns = [
    path('', BaseListView.as_view(), name = 'base-view'),
    path('like/', LikeToggleView.as_view(), name='like-toggle'),

    path('comment-delete/<int:pk>', CommentDeleteView.as_view(), name='delete-comment'),
    path('comment-update/<int:pk>', CommentUpdateView.as_view(), name='update-comment'),

    path('add-comment/', CreateCommentView.as_view(), name='add_comment'),
    path('<str:category_slug>/<str:brand_slug>/', BrandDetailView.as_view(), name = 'brand-detail'),
    path('<str:category_slug>', CategoryDetailView.as_view(), name = 'category-detail'),
    path('<str:category_slug>/<str:product_slug>', ProductDetailView.as_view(), name = 'product-detail'),



]