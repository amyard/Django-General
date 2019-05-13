from django.views.generic.list import MultipleObjectMixin
from engine.projects.models import Project
from django.db.models import Count, Q
from datetime import date


class MainPageListMixin(MultipleObjectMixin):

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['projects'] = Project.objects.filter(user=self.request.user)
        context['count_tasks'] = Project.objects.filter(user=self.request.user).annotate(
            count=Count('project__title', filter=Q(project__status=0) & Q(project__timestamp__gte=date.today()))).values('title', 'count')

        return context