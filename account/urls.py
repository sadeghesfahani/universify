from django.urls import path
from .views import *

app_name = 'account'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('', AccountView.as_view(), name='account'),
    path('logout', logOutHandler, name='logout'),

]
