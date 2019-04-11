from .models import Project
from bootstrap_modal_forms.forms import BSModalForm

class ProjectForm(BSModalForm):

    class Meta:
        model = Project
        fields = ['title', 'color']