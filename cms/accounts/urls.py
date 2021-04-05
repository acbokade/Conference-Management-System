from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signup_process', views.singup_process, name='signup_process'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('change_password_process', views.change_password_process, name='change_password_process'),
]