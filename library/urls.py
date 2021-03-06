from django.urls import path
from .views import *

urlpatterns = [
    path('', BookList.as_view(), name='library'),
    path('lendout', HandleLendOut.as_view(), name='lendout'),
    path('dashboard', UserDashboard.as_view(), name='dashboard'),
    path('renewal', HandleRenewal.as_view(), name='renewal'),
    path('return', HandelReturn.as_view(), name='return'),

]
