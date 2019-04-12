# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from projects.models import Project
from tasks.models import Task

from datetime import date, timedelta


# @login_required(login_url="/accounts/login/")
# def home(request):
#     return render(request, 'todo_core/main.html', {'info': 'It\'s working.'})




class MainPageListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'core/main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageListView, self).get_context_data(*args, **kwargs)

        context['projects'] = self.model.objects.filter(user = self.request.user)
        context['tasks'] = Task.objects.filter(project__user= self.request.user, timestamp=date.today(), status=0)
        context['date'] = date.today()
        return context