from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import LoginForm



class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = 'account'


class AccountView(TemplateView):
    template_name = 'account/index.html'