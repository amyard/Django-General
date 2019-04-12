from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Project
from .forms import ProjectForm, ProjectUpdateForm

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView



#############################################################################################
##    CATEGORY VIEWS
#############################################################################################


class ProjectCreateView(BSModalCreateView):
    template_name = 'projects/actions/category-create.html'
    form_class = ProjectForm
    success_message = 'Success: Project was created.'
    success_url = reverse_lazy('core:base-view')


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)



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
    success_url = reverse_lazy('core:base-view')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        return kwargs
