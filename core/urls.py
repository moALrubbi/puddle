from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('statistics/', views.statistics, name='statistics'),  # Add the URL pattern for 'statistics' view
    path('api/statistics/', views.statistics_api_view, name='statistics-api'),  # Add the URL pattern for 'statistics' API view
    path('api/signup/', views.register, name='register'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/user/', views.get_user, name='user'),

]
