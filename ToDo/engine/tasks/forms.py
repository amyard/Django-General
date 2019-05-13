from engine.tasks.models import Task
from engine.projects.models import Project

from bootstrap_modal_forms.forms import BSModalForm
from django import forms


class TaskForm(BSModalForm):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Task name'}))
    timestamp = forms.DateField(label='', widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    description = forms.CharField(required=False, label = '', widget = forms.Textarea(attrs = {'class':'form-control', 'rows': 4, 'cols':100, 'placeholder': 'Type detail information about task'}))
    priority = forms.Select()


    class Meta:
        model = Task
        fields = ['project', 'title', 'priority', 'description', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(queryset = Project.objects.filter(user=self.request.user))
        self.fields['project'].label=''
        self.fields['priority'].label = ''


    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        title = cleaned_data.get('title')
        timestamp = cleaned_data.get('timestamp')
        if Task.objects.filter(title=title, project__user = self.user, timestamp = timestamp, status=0).exists():
            raise forms.ValidationError('Such task already exists that day.')
        return cleaned_data


class TaskUpdateForm(BSModalForm):

    title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Task name'}))
    timestamp = forms.DateField(label='', widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}))
    description = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Type detail information about task'}))
    priority = forms.Select()


    class Meta:
        model = Task
        fields = ['project', 'title', 'priority', 'description', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        self.pk = kwargs.pop('pk', '')
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(queryset=Project.objects.filter(user=self.request.user))
        self.fields['project'].label = ''
        self.fields['priority'].label = ''


    def clean(self):
        cleaned_data = super(TaskUpdateForm, self).clean()
        title = cleaned_data.get('title')
        timestamp = cleaned_data.get('timestamp')
        if Task.objects.exclude(pk=self.pk).filter(title=title, project__user = self.user, timestamp = timestamp, status=0).exists():
            raise forms.ValidationError('Such task already exists that day.')
        return cleaned_data