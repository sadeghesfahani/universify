from django.contrib.auth import login, logout
from django.core.checks.translation import check_setting_languages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import LoginForm, RegisterForm
from .models import *
from .serializers import DepartmentSerializer, PositionSerializer


class LoginView(FormView):
    template_name = 'account/login.html'
    form_class = LoginForm

    # success_url = reverse_lazy('account')

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

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse_lazy('account:account')


def logOutHandler(request):
    logout(request)
    return HttpResponseRedirect(reverse('account:account'))


class AccountView(TemplateView):
    template_name = 'account/index.html'


class RegisterView(FormView):
    template_name = 'account/register.html'
    extra_context = {'faculties': Faculty.objects.all(), 'departments': Department.objects.all()}
    form_class = RegisterForm
    success_url = reverse_lazy('account')

    def get_context_data(self, *args, **kwargs):
        context = super(RegisterView, self).get_context_data(*args, **kwargs)
        context['faculties'] = Faculty.objects.all()
        context['departments'] = Department.objects.all()
        return context

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return HttpResponseRedirect(reverse('account'))
    #     return super(RegisterView, self).dispatch(request, *args, **kwargs)
    #
    # def form_valid(self, form):
    #     login(self.request, form.getUser())
    #     return super(RegisterView, self).form_valid(form)
    #
    # def form_invalid(self, form):
    #     self.extra_context = {'error': True}
    #     return super(RegisterView, self).form_invalid(form)


class DepartmentList(APIView):

    def get_departments(self, faculty):
        return Department.objects.filter(faculty__name=faculty)

    def get(self, request, faculty):
        departments = self.get_departments(faculty)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


class PositionList(APIView):

    def get_positions(self, department):
        return Position.objects.filter(department__name=department)

    def get(self, request, department):
        positions = self.get_positions(department)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)
