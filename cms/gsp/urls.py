from django.urls import path

from . import views

urlpatterns = [
    path('redirect_signup', views.redirect_signup, name='redirect_signup'),
    path('redirect_login', views.redirect_login, name='redirect_login'),
    path('redirect_logout', views.redirect_logout, name='redirect_logout'),
    path('redirect_userpage', views.redirect_userpage, name='redirect_userpage'),
    path('<str:conf_name>/new_submission/', views.render_gsp),
    path('<str:conf_name>/existing_conf_submissions', 
        views.existing_conf_submissions, 
        name='existing_conf_submissions'
    ),
    path('<str:conf_name>/<str:paper_title>/edit', views.edit_submission),
    path('<str:conf_name>/<str:paper_title>/withdraw', views.withdraw_submission),
]