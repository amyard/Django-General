from django.contrib.auth.views import LogoutView
from django.contrib import messages



class CustomLogoutView(LogoutView):

    def get_next_page(self):
        next_page = super(CustomLogoutView, self).get_next_page()
        messages.add_message(self.request, messages.SUCCESS, 'You successfully log out!')
        return next_page