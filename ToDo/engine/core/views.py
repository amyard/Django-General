from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from engine.core.mixins import MainPageListMixin

from engine.projects.models import Project
from engine.tasks.models import Task

from datetime import date, timedelta




# from django.contrib.auth.decorators import login_required
# @login_required(login_url="/accounts/login/")
# def home(request):
#     return render(request, 'todo_core/main.html', {'info': 'It\'s working.'})




class MainPageListView(LoginRequiredMixin, ListView, MainPageListMixin):
    model = Project
    template_name = 'core/main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageListView, self).get_context_data(*args, **kwargs)
        context['tasks'] = Task.objects.filter(project__user= self.request.user, timestamp=date.today(), status=0)
        context['date'] = date.today()
        return context



class NextSevenDaysView(LoginRequiredMixin, ListView, MainPageListMixin):
    model = Project
    template_name = 'core/sevendays.html'
    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=8)

    def get_context_data(self, *args, **kwargs):
        context = super(NextSevenDaysView, self).get_context_data(*args, **kwargs)
        context['tasks'] = Task.objects.filter(project__user__username=self.request.user, status=0, timestamp__range=(self.start_date, self.end_date))
        context['dates'] = [(date.today() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, 8)]
        return context