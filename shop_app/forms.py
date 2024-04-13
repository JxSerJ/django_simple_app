import datetime

from django import forms


class ProductForm(forms.Form):
    id = forms.IntegerField(label='Product ID')
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Enter Product description'
    }))
    price = forms.DecimalField(max_digits=1000, decimal_places=2)
