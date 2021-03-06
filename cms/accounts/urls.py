from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signup_process', views.singup_process, name='signup_process'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('delete_account', views.delete_account, name='delete_account'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('make_new_password_process', views.make_new_password_process, name='make_new_password_process'),
    path('conferences', views.redirect_conference),
    path('assigned_papers', views.redirect_assigned_papers),
    path('my_conferences', views.redirect_my_conference),
    path('profile', views.profile, name='profile'),
    path('userpage', views.userpage, name='userpage'),
    path('change_password', views.change_password, name='change_password'),
    path('change_password_process', views.change_password_process, name='change_password_process'),
    path('complete_research_profile', views.complete_research_profile, name='complete_research_profile'),
    path('complete_research_profile_process', views.complete_research_profile_process,
         name='complete_research_profile_process'),
]