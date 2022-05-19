from django.urls import path
from . import views


app_name = 'finance'

urlpatterns = [

    path('', views.index, name='index'),
    path('not-paid/', views.not_paid, name='not-paid'),
    path('statistics/', views.statistics, name='statistics'),
]
