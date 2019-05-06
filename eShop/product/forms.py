from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Like, Product, Comment

from bootstrap_modal_forms.forms import BSModalForm

User = get_user_model()


class LikeForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    product = forms.ModelChoiceField(Product.objects.all(), required=False)
    ip = forms.GenericIPAddressField(required=False)


class CommentForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Введите ваш комментарий'}))

    class Meta:
        model = Comment
        fields = ['text']



class CommentFormModal(BSModalForm):
    text = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Введите ваш комментарий'}))

    class Meta:
        model = Comment
        fields = ['text']