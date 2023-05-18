from django import forms 
from .models import PayModel

class PaymentForm(forms.ModelForm):
    class Meta:
        model = PayModel
        fields = ('amount','email','account','bank_code','card_details')