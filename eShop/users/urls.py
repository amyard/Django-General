from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from users.views import *


app_name = 'accounts'

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('product:base-view')), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', RegistrationView.as_view(), name='signup'),

    # RESET PASSWORD
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/reset_password/password_reset.html',
                                                                 email_template_name='users/reset_password/password_reset_email.html',
                                                                 subject_template_name='users/reset_password/password_reset_subject.txt',
                                                                 success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password/password_reset_confirm.html',
                                                     success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password/password_reset_complete.html'),
        name='password_reset_complete'),
]