from django.urls import path

from . import views

urlpatterns = [
    path('<str:event_id>/new_submission/', views.render_gsp),
    path('<str:conf_name>/existing_conf_submissions', 
        views.existing_conf_submissions, 
        name='existing_conf_submissions'
    ),
]