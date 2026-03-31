from django import forms
from .models import UniformItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Inventory form (keep this!)
class UniformItemForm(forms.ModelForm):
    class Meta:
        model = UniformItem
        fields = ['name', 'size', 'quantity', 'price']

# User registration form (new)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # optional

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']