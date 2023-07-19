from django.urls import path
from django.conf.urls import handler404, handler500
from . import views

app_name = "happyphoto"

urlpatterns = [
    path('', views.home, name = 'home'),
    
]

handler404 = 'backend.happyphoto.views.handler404'
handler500 = 'backend.happyphoto.views.server_error'