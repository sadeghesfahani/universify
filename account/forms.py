from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=15, label='شناسه کاربری')
    password = forms.CharField(max_length=40, widget=forms.PasswordInput, label='کلمه عبور')

    def is_valid(self):
        super(LoginForm, self).is_valid()
        user = authenticate(identifier=self.cleaned_data['identifier'], password=self.cleaned_data['password'])
        print(user)
        return True if user is not None else False

    def getUser(self):
        return authenticate(identifier=self.cleaned_data['identifier'], password=self.cleaned_data['password'])
