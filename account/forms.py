from django import forms
from django.contrib.auth import authenticate

from account.models import User, CustomUserManager, Faculty, Department, Position


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
    email = forms.EmailField(label='ایمیل')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='رمز عبور')
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='تکرار رمز عبور')

    def matchPass(self):
        return self.cleaned_data['password'] == self.cleaned_data['confirm_password']

    def is_valid(self):
        super(RegisterForm, self).is_valid()
        return self.matchPass()

    def get_position(self):
        try:
            faculty = Faculty.objects.get(name=self.data['faculty'])
            department = Department.objects.get(name=self.data['department'], faculty_id=faculty.id)
            position = Position.objects.get(name=self.data['position'], department_id=department.id)
        except:
            position = None
        return position

    def addUser(self):
        user = User(first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'],
                    position=self.get_position(),email=self.cleaned_data['email'])

        user.set_password(self.cleaned_data['password'])
        user.save()