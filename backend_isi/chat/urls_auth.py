from django.urls import path
from . import views_auth
from .views import home_view


urlpatterns = [
    path('register/', views_auth.register_view, name='register'),
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('', home_view, name='home'),
]