from django.urls import path

from . import views

urlpatterns = [
    path('<str:event_id>/new_submission/', views.render_gsp)
]