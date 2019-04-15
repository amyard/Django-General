from django.urls import path
from .views import *



urlpatterns = [
    path('', MainPageListView.as_view(), name = 'base-view'),
    path('nextweek', NextSevenDaysView.as_view(), name = 'next-week'),
]
