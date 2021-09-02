from django.urls import path
from .views import *

urlpatterns = [
    path('', BookList.as_view(), name='library'),
    path('lendout/<int:book_id>', HandleLendOut.as_view(), name='lendout'),

]
