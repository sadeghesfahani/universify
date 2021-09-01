from django import forms


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=15, label='شناسه کاربری')
    password = forms.CharField(max_length=40, widget=forms.PasswordInput, label='کلمه عبور')
