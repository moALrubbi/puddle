# checkout/forms.py
from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    street_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder': 'Your street name',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Your postal code',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    building_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Your builed number',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    town_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your town/city',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Your phone number',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
    delivery_info = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Additional Delivery Information',
        'class': 'w-full py-2 px-4 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500'
    }))
