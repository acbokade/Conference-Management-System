from django.urls import path
from . import views

urlpatterns = [
    path('redirect_signup', views.redirect_signup, name='redirect_signup'),
    path('redirect_login', views.redirect_login, name='redirect_login'),
    path('redirect_logout', views.redirect_logout, name='redirect_logout'),
    path('redirect_userpage', views.redirect_userpage, name='redirect_userpage'),
    path('assigned_papers', views.assigned_papers, name='assigned_papers'),
    path('<str:conf_name>/apply_as_a_reviewer', views.apply_as_a_reviewer,
         name='apply_as_a_reviewer'),
    path('<str:conf_name>/make_review/<str:title>',
         views.make_review, name='make_review'),
    path('<str:conf_name>/edit_review/<str:title>',
         views.edit_review, name='edit_review'),
    path('<str:conf_name>/invite_reviewers/',
         views.invite_reviewers, name='invite_reviewers'),
    path('<str:conf_name>/automated_reviewer_assignment/',
         views.automated_reviewer_assignment, name='automated_reviewer_assignment'),
    path('<str:conf_name>/manual_reviewer_assignment/',
         views.manual_reviewer_assignment, name='manual_reviewer_assignment'),
]
