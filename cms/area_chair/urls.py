from django.urls import path
from . import views

urlpatterns = [
    path('redirect_signup', views.redirect_signup, name='redirect_signup'),
    path('redirect_login', views.redirect_login, name='redirect_login'),
    path('redirect_logout', views.redirect_logout, name='redirect_logout'),
    path('redirect_userpage', views.redirect_userpage, name='redirect_userpage'),
    # path('assigned_papers', views.assigned_papers, name='assigned_papers'),
    path('<str:conf_name>/select_area_chair', views.select_area_chair,
         name='select_area_chair'),
    path('<str:conf_name>/assign_acs', views.assign_area_chairs),
    path('<str:conf_name>/make_decision/<str:title>',
         views.make_ac_decision, name='make_review'),
    path('<str:conf_name>/edit_decision/<str:title>',
         views.edit_ac_decision, name='edit_review'),
]
