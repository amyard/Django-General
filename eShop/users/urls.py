from django.urls import path, reverse_lazy
from users.views import *


app_name = 'users'

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('product:base-view')), name='logout'),

]