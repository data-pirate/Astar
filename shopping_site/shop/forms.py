from django import forms
from django_countries.fields import CountryField

class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input'
    }))
    address1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input',
        'id':"checkout_address"
    }))
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input',
        'id': "checkout_address_2"
    }), required=False)
    company = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'checkout_input'
    }) , required=False)
    country = CountryField(blank_label='Select country')
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'State...',
        'class': 'checkout_input'
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123456',
        'class': 'checkout_input'
    }))

    terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'billing_checkbox',
        'id': 'cb_1'
    }))

    newsletter = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'billing_checkbox',
        'id': 'cb_3'
    }))

    method_of_payment = forms.BooleanField(widget=forms.RadioSelect())
    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': '(1234) 567-789',
        'class': 'checkout_input'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'your_email@example.com',
        'class': 'checkout_input'
    }))