from .models import Project
from bootstrap_modal_forms.forms import BSModalForm
from django import forms



class ProjectForm(BSModalForm):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Type new project'}))
    color = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Choose the color'}))

    class Meta:
        model = Project
        fields = ['title', 'color']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)


    def clean_title(self):
        title = self.cleaned_data['title']
        if Project.objects.filter(title=title, user = self.user).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title


    def clean_color(self):
        color = self.cleaned_data['color']
        if Project.objects.filter(color=color, user = self.user).exists():
            raise forms.ValidationError('You cann\'t use this color again.')
        return color



class ProjectUpdateForm(BSModalForm):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Type new project'}))
    color = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Choose the color'}))

    class Meta:
        model = Project
        fields = ['title', 'color']

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.user = kwargs.pop('user')
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data['title']
        color = self.cleaned_data['color']

        if Project.objects.exclude(pk=self.pk).filter(title=title, user = self.user).exists():
            raise forms.ValidationError('You cann\'t use this title again.')

        if Project.objects.exclude(pk=self.pk).filter(color=color, user = self.user).exists():
            raise forms.ValidationError('You cann\'t use this color again.')
