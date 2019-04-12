from django.urls import path
from .views import *



urlpatterns = [
    path('create', ProjectCreateView.as_view(), name='create-project'),
    path('delete/<int:pk>', ProjectDeleteView.as_view(), name='delete-project'),
    path('update/<int:pk>', ProjectUpdateView.as_view(), name='update-project'),
]


