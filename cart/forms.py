# forms.py
from django import forms
from django import forms

class BillingForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=20)
    address_line1 = forms.CharField(max_length=100)
    address_line2 = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)
    total_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)  # Optional

