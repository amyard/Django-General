from django.urls import path
from .views import *



urlpatterns = [
    path('', MainPageListView.as_view(), name = 'base-view'),
    path('create-project', ProjectCreateView.as_view(), name='create-project'),
]
