from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Project


# @login_required(login_url="/accounts/login/")
# def home(request):
#     return render(request, 'todo_core/main.html', {'info': 'It\'s working.'})




class MainPageListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'todo_core/main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageListView, self).get_context_data(*args, **kwargs)

        context['projects'] = self.model.objects.all()
        return context



