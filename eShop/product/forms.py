from django import forms
from django.contrib.auth import get_user_model

from django.conf import settings
from .models import Like, Product, Comment


User = get_user_model()


class LikeForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    product = forms.ModelChoiceField(Product.objects.all(), required=False)
    ip = forms.GenericIPAddressField(required=False)


class CommentForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 100, 'placeholder': 'Type the comment'}))

    class Meta:
        model = Comment
        fields = ['text']