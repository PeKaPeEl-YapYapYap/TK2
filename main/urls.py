from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/google/', views.login_google, name='login_google'),
    path('login/google/callback/', views.login_google_callback, name='login_google_callback'),
    path('logout/', views.logout_user, name='logout'),
]
