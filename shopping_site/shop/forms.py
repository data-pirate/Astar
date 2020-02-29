from django import forms
from .models import Item
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_OPTIONS = (
    ('paypal', 'Paypal'),
    ('stripe', 'Stripe'),
    ('cod', 'Cash On Delivery'),
    ('credit', 'Credit card'),
    ('dbt', 'Direct Bank Transfer')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input'
    }))

    address1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input m-2',
    }))

    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input m-2',
    }), required=False)

    company = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'checkout_input'
    }), required=False)

    country = CountryField(blank_label='Select country ...').formfield(widget=CountrySelectWidget(attrs={
        'class': 'dropdown_item_select checkout_input countries order-alpha'
    }))

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123456',
        'class': 'checkout_input'
    }))

    terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'billing_checkbox',
    }))

    newsletter = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'billing_checkbox',
    }))

    method_of_payment = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)

    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'billing_checkbox',
    }))

    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': '(1234) 567-789',
        'class': 'checkout_input'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'your_email@example.com',
        'class': 'checkout_input'
    }))


class AddProduct(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title',
            'price',
            'discount_price',
            'category',
            'sub_category',
            'label',
            'description',
            'slug'
        )
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_category': forms.TextInput(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
        }
