# urls.py
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'(?i)^signup\/?', views.signup, name='signup'),
    re_path(r'(?i)^login\/?', views.login, name='login'),
    re_path(r'(?i)^test_token\/?', views.protected_view, name='test_token')
]
