from django.urls import path
from .views import *

urlpatterns = [
    path('', BookList.as_view(), name='library'),

]
