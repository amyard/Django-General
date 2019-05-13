from engine.users.views import *

from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView


from django.contrib.auth import views as auth_views


urlpatterns = [

    path('login/', LoginView.as_view(), name ='login-view'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('core:base-view')), name ='logout-view'),

    # registration
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # delete user account
    path('delete/<int:pk>', UserAccountDeleteView.as_view(), name='delete-user-account'),

    # reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/actions/password_reset.html',
                                                                 email_template_name='users/actions/password_reset_email.html',
                                                                 subject_template_name='users/actions/password_reset_subject.txt',
                                                                 success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/actions/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/actions/password_reset_confirm.html',
                                                     success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/actions/password_reset_complete.html'),
         name='password_reset_complete'),

]