from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signup_process', views.singup_process, name='signup_process'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('conferences', views.redirect_conference),
    path('profile', views.profile, name='profile'),
    path('userpage', views.userpage, name='userpage'),
    path('change_password', views.change_password, name='change_password'),
    path('change_password_process', views.change_password_process, name='change_password_process'),
    path('complete_research_profile', views.complete_research_profile, name='complete_research_profile'),
    path('complete_research_profile_process', views.complete_research_profile_process,
         name='complete_research_profile_process'),
]