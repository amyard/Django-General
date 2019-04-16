from django.urls import path
from .views import *



urlpatterns = [
    path('create', TaskCreateView.as_view(), name='create-task'),
    path('delete/<int:pk>', TaskDeleteView.as_view(), name='delete-task'),
    path('update/<int:pk>', TaskUpdateView.as_view(), name='update-task'),
    path('read/<int:pk>', TaskReadView.as_view(), name='read-task'),
    path('done/<int:pk>', DoneView.as_view(), name='done-task'),
]