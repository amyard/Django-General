from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views import View
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

from engine.users.forms import LoginForm, RegistrationForm




User = get_user_model()

class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm
	message_send = 'You are logged in.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			log_user = User.objects.get(email = email)

			user = authenticate(username = log_user.username, password = password)
			if user:
				login(self.request, user)
				messages.success(self.request, self.message_send)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)





######################################################################################
#   SIGN UP WITH EMAIL CONFIRMATION
######################################################################################

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from engine.users.forms import RegistrationForm
from engine.users.tokens import account_activation_token



User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password']
            user.set_password(password)
            password_check = form.cleaned_data['password_check']
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/actions/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'users/actions/confirm_email.html', {})
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/actions/confirm_email_valid.html', {})
    else:
        return render(request, 'users/actions/confirm_email_invalid.html', {})



######################################################################################
#   DELETE USER ACCOUNT WITH MODAL
######################################################################################

from bootstrap_modal_forms.generic import BSModalDeleteView
from django.urls import reverse_lazy


class UserAccountDeleteView(BSModalDeleteView):
    model = User
    template_name = 'users/actions/user-account-delete.html'
    success_message = 'Success: User Account was deleted.'
    success_url = reverse_lazy('todo:base-view')