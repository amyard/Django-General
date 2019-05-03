from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.views.generic import View, CreateView
from django.urls import reverse_lazy

from users.forms import LoginForm, RegistrationForm


class CustomLogoutView(LogoutView):

    def get_next_page(self):
        next_page = super(CustomLogoutView, self).get_next_page()
        messages.add_message(self.request, messages.SUCCESS, 'You successfully log out!')
        return next_page




class LoginView(View):
    template_name = 'users/login.html'
    form = LoginForm
    message_send = 'Вы вошли в систему.'

    def get(self, request, *args, **kwargs):
        form = self.form
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                login(self.request, user)
                messages.success(self.request, self.message_send)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(self.request, self.template_name, context)



class RegistrationView(CreateView):
    template_name = 'users/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('accounts:login')