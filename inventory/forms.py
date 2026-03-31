from django import forms
from .models import UniformItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Inventory form
class UniformItemForm(forms.ModelForm):
    class Meta:
        model = UniformItem
        fields = ['name', 'size', 'quantity', 'price']

# User registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email'] # Password fields are handled automatically