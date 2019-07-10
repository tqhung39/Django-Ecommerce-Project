from django import forms
from .models import Order
from django_countries.widgets import CountrySelectWidget
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address','city','country']
        widgets = {'country': CountrySelectWidget()}

class RefundForm(forms.Form):
    refund_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))