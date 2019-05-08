from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from core.product.models import Like, Product, Comment

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




class FilterProduct(forms.Form):

    comments_choices = (
        (1, ''),
        (2, 'Продукты без коментариев'),
        (3, "Продукты с комментариями")
    )

    like_choices = (
        (1, ''),
        (2, 'Продукты, которым не поставили "Like"'),
        (3, 'Продукты, которым поставили "Like"')
    )

    price_from = forms.IntegerField(label='Цена', required=False,
                                    widget=forms.NumberInput(attrs={'placeholder': 'Цена от'}))
    price_to = forms.IntegerField(label='', required=False,
                                  widget=forms.NumberInput(attrs={'placeholder': 'Цена до'}))
    comments = forms.ChoiceField(label='Комментарии', choices=comments_choices, required=False, widget=forms.Select())
    likes = forms.ChoiceField(label='Лайк', choices=like_choices, required=False, widget=forms.Select())