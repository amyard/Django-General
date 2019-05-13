from django.views.generic import ListView
from engine.core.mixins import MainPageListMixin


from engine.projects.models import Project
from engine.projects.forms import ProjectForm, ProjectUpdateForm
from engine.tasks.models import Task

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView
from datetime import date


class ProjectCreateView(BSModalCreateView):
    template_name = 'projects/actions/category-create.html'
    form_class = ProjectForm
    success_message = 'Success: Project was created.'


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')



class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = 'projects/actions/category-delete.html'
    success_message = 'Success: Project was deleted.'
    success_url = reverse_lazy('core:base-view')



class ProjectUpdateView(BSModalUpdateView):
    model = Project
    template_name = 'projects/actions/category-update.html'
    form_class = ProjectUpdateForm
    success_message = 'Success: Project was updated.'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')


class ProjectListView(ListView, MainPageListMixin):
    model = Project
    template_name = 'projects/detail-projects.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectListView, self).get_context_data(*args, **kwargs)
        ids = self.kwargs.get('pk')
        context['title'] = self.kwargs.get('title')
        context['tasks'] = Task.objects.filter(timestamp__gte=date.today(), status=0,project__user=self.request.user, project__id = ids)
        context['dates'] = Task.objects.filter(timestamp__gte=date.today(), status=0,project__user=self.request.user, project__id = ids).values('timestamp').distinct()
        return context