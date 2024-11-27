from django.urls import path
from . import admin_views
from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)



urlpatterns = [
    path('api/login/', admin_views.admin_login_view, name='admin_login' ),
    path('api/test/', admin_views.test_admin, name='test_admin'),
    path('api/logout/', admin_views.admin_logout_view, name='admin_logout' ),
    path('login/', admin_views.login_page, name='login_page'),
    path('administration/', admin_views.custom_admin_view, name='administration'),
    path('', admin.site.urls),
]