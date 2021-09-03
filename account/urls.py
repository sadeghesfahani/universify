from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'account'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('', AccountView.as_view(), name='account'),
    path('logout', logOutHandler, name='logout'),
    path('department-list/<str:faculty>/', DepartmentList.as_view(), name='department-list'),
    path('position-list/<str:department>/', PositionList.as_view(), name='position-list')
]
