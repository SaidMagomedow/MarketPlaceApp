from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *
from django.contrib.auth.models import User


# Данная форма будет проверять данные отправленые пользователем при заполнении формы заказа
class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'
# order_date делает так что бы в checkout.html поле с указание даты доставки было легким для заполнения ,
# то есть добавляет календарь
    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment')
