from django import forms
from django.contrib.auth import get_user_model

from django.conf import settings
from .models import Like, Product


User = get_user_model()


class LikeForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    product = forms.ModelChoiceField(Product.objects.all(), required=False)
    ip = forms.GenericIPAddressField(required=False)