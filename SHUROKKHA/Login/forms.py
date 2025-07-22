from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
class CustomUserCreationForm(forms.ModelForm): #add operator
    class Meta:
        model = User
        fields = ['username', 'email', 'division', 'is_active'] #takes attributes from custom model file of user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role','division','is_active') #edit operator
class UserIDLoginForm(forms.Form):
    user_id = forms.IntegerField(label="User ID")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)#custom form as django builtin username