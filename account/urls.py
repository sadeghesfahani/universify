from django.urls import path
from .views import *

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('', AccountView.as_view(), name='account'),
    path('logout', logOutHandler, name='logout'),

]
