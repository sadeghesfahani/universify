from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=15, label='شناسه کاربری')
    password = forms.CharField(max_length=40, widget=forms.PasswordInput, label='کلمه عبور')

    def is_valid(self):
        super(LoginForm, self).is_valid()
        try:
            user = authenticate(identifier=self.cleaned_data['identifier'], password=self.cleaned_data['password'])
            return True if user is not None else False
        except ValueError:
            return False

    def getUser(self):
        return authenticate(identifier=self.cleaned_data['identifier'], password=self.cleaned_data['password'])


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=60, label='نام')
    last_name = forms.CharField(max_length=100, label='نام خانوادگی')
