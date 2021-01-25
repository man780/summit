from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'teacher'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/<int:id>/', views.student, name='student'),
    path('group-students/<int:id>/', views.group_students, name='student'),
]
