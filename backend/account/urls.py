from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm

app_name = "account"

urlpatterns = [
    path('', views.register, name = 'sign_up'),
    # LOGIN & LOGOUT
    path('sign-in/', auth_views.LoginView.as_view(template_name = 'account/sign_in.html',
    form_class = UserLoginForm), name = 'sign_in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page = '/'), name = 'sign_out'),
    # END LOGIN & LOGOUT

    path('profiles/', views.profiles, name = 'profiles'),
    path('dashboard/<str:id>/', views.dashboard, name = 'my_dashboard'),

    
]