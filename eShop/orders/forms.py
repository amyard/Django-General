from django import forms
from orders.models import Order


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class OrderCreateForm(forms.ModelForm):\


    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '::')
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            Row(
                Column('address', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('postal_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Оплатить')
        )

