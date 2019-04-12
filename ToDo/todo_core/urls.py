from django.urls import path
from .views import *



urlpatterns = [
    path('', MainPageListView.as_view(), name = 'base-view'),
    path('create-project', ProjectCreateView.as_view(), name='create-project'),
    path('delete-project/<int:pk>', ProjectDeleteView.as_view(), name='delete-project'),
    path('update-project/<int:pk>', ProjectUpdateView.as_view(), name='update-project'),
]


