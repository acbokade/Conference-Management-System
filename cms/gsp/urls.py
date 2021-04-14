from django.urls import path

from . import views

urlpatterns = [
    path('<str:conf_name>/new_submission/', views.render_gsp),
    path('<str:conf_name>/existing_conf_submissions', 
        views.existing_conf_submissions, 
        name='existing_conf_submissions'
    ),
    path('<str:conf_name>/<str:paper_title>/edit', views.edit_submission),
    path('<str:conf_name>/<str:paper_title>/withdraw', views.withdraw_submission),
]