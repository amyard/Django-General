from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView



urlpatterns = [

    path('login/', LoginView.as_view(), name ='login-view'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('todo:base-view')), name ='logout-view'),
    # path('registration/', RegistrationView.as_view(), name = 'registration-view'),

    # registration
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]