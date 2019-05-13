from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse_lazy

from engine.tasks.models import Task
from engine.tasks.forms import TaskForm, TaskUpdateForm

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView, BSModalReadView



class TaskCreateView(BSModalCreateView):
    template_name = 'tasks/actions/task-create.html'
    form_class = TaskForm
    success_message = 'Success: Task was created.'


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(TaskCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')





class TaskUpdateView(BSModalUpdateView):
    model = Task
    template_name = 'tasks/actions/task-update.html'
    form_class = TaskUpdateForm
    success_message = 'Success: Task was updated.'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(TaskUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')



class TaskDeleteView(BSModalDeleteView):
    model = Task
    template_name = 'tasks/actions/task-delete.html'
    success_message = 'Success: Task was deleted.'
    success_url = reverse_lazy('core:base-view')



class TaskReadView(BSModalReadView):
    model = Task
    template_name = 'tasks/actions/task-read.html'




class DoneView(View):
    model = Task
    template_name = 'core/main.html'


    def get(self, reguest, **kwargs):
        pk = self.kwargs.get('pk')
        self.model.objects.filter(id = pk)
        self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
        return render(self.request, self.request.session['report_url'])

    def get(self, reguest, **kwargs):
        pk = self.kwargs.get('pk')
        self.model.objects.filter(id = pk).update(status = 1)
        self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(self.request.session['report_url'])


