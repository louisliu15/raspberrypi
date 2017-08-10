from django import forms
from django.contrib.auth.forms import UserCreationForm
from Web_Server.models import Ruser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': 'Username', "required": "required", 'type': 'username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': 'Password', "required": "required"}))


class RegisterForm(UserCreationForm):
    class Meta:
        model = Ruser
        fields = ["username", "password1", "password2", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})