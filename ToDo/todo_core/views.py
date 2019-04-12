from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Project
from .forms import ProjectForm, ProjectUpdateForm

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView, BSModalUpdateView



# @login_required(login_url="/accounts/login/")
# def home(request):
#     return render(request, 'todo_core/main.html', {'info': 'It\'s working.'})




class MainPageListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'todo_core/main.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MainPageListView, self).get_context_data(*args, **kwargs)

        context['projects'] = self.model.objects.filter(user = self.request.user)
        return context



#############################################################################################
##    CATEGORY VIEWS
#############################################################################################


class ProjectCreateView(BSModalCreateView):
    template_name = 'todo_core/actions/category-create.html'
    form_class = ProjectForm
    success_message = 'Success: Project was created.'
    success_url = reverse_lazy('todo:base-view')


    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)



class ProjectDeleteView(BSModalDeleteView):
    model = Project
    template_name = 'todo_core/actions/category-delete.html'
    success_message = 'Success: Project was deleted.'
    success_url = reverse_lazy('todo:base-view')



class ProjectUpdateView(BSModalUpdateView):
    model = Project
    template_name = 'todo_core/actions/category-update.html'
    form_class = ProjectUpdateForm
    success_message = 'Success: Project was updated.'
    success_url = reverse_lazy('todo:base-view')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        return kwargs
