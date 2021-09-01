from django.contrib.auth import login, logout
from django.core.checks.translation import check_setting_languages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from .forms import LoginForm


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('account')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('account'))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.getUser())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        self.extra_context = {'error': True}
        return super(LoginView, self).form_invalid(form)


def logOutHandler(request):
    logout(request)
    return HttpResponseRedirect(reverse('account'))


class AccountView(TemplateView):
    template_name = 'account/index.html'
