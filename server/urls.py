# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login', views.login, name='login'),  # Add the login URL pattern
    path('signup', views.signup),  # Allow URL without trailing slash
    path('test_token', views.protected_view)
]
