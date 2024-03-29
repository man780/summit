from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from courses.views import CourseListView


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('main/', include('reception.urls')),
    path('finance/', include('finance.urls')),
    path('admin/', admin.site.urls),
    path('teacher/', include('teacher.urls')),
    path('course/', include('courses.urls')),
    path('', CourseListView.as_view(), name='course_list'),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

handler500 = 'reception.views.main.error_500'
handler404 = 'reception.views.main.error_404'
