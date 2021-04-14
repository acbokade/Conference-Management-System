from django.urls import path
from . import views

urlpatterns = [
    path('redirect_signup', views.redirect_signup, name='redirect_signup'),
    path('redirect_login', views.redirect_login, name='redirect_login'),
    path('redirect_logout', views.redirect_logout, name='redirect_logout'),
    path('redirect_userpage', views.redirect_userpage, name='redirect_userpage'),
    path('list_conferences', views.list_conferences, name='list_conferences'),
    path('list_my_conferences', views.list_my_conferences, name='list_my_conferences'),
    path('create_conference', views.create_conference, name='create_conference'),
    path('update_conference/<str:name>',
         views.update_conference, name='update_conference'),
    path('create_workshop', views.create_workshop, name='create_workshop'),
    path('update_workshop/<str:name>',
         views.update_conference, name='update_workshop'),
     path('details/<conf_name>', views.conference_details),

]
