from django.urls import path
from . import views


app_name = 'teacher'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/<int:id>/', views.student, name='student'),
    path('group-students/<int:group_id>/', views.group_students, name='group-students'),
]
