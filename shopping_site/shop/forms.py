from django import forms
from .models import Item, Profile
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User

PAYMENT_OPTIONS = (
    ('paypal', 'Paypal'),
    ('stripe', 'Stripe'),
    ('cod', 'Cash On Delivery'),
    ('credit', 'Credit card'),
    ('dbt', 'Direct Bank Transfer')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    address1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control m-2',
    }))

    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control m-2',
    }), required=False)

    company = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)

    country = CountryField(blank_label='Select country ...').formfield(widget=CountrySelectWidget(attrs={
        'class': 'dropdown_item_select form-control countries order-alpha'
    }))

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '123456',
        'class': 'form-control'
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
        'class': 'form-control'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'your_email@example.com',
        'class': 'form-control'
    }))


CATEGORY_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women')
)

SUB_CATEGORY = (
    ('shirts', 'Shirts'),
    ('dress', 'Dresses'),
    ('jeans', 'Jeans'),
    ('shoes', 'Shoes'),
    ('purse', 'Purse')
)
LABELS = (
    ('hot', 'Hot'),
    ('new', 'New'),
    ('sale', 'Sale')
)


class AddProduct(forms.ModelForm):
    category = forms.ChoiceField(label='category' ,choices=CATEGORY_CHOICES, required=True),
    sub_category = forms.ChoiceField(choices=SUB_CATEGORY, required=True),
    label = forms.ChoiceField(choices=LABELS, required=False)

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
        )
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'md-textarea form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditProduct(forms.ModelForm):
    category = forms.ChoiceField(label='category' ,choices=CATEGORY_CHOICES, required=True),
    sub_category = forms.ChoiceField(choices=SUB_CATEGORY, required=True),
    label = forms.ChoiceField(choices=LABELS, required=False)

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
        )
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'class': 'md-textarea form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    dob = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    photo = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Profile
        exclude = (
            'user',
        )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control validate'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control validate'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control validate'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control validate'}),
        }