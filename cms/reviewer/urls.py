from django.urls import path
from . import views

urlpatterns = [
    path('<str:conf_name>/apply_as_a_reviewer', views.apply_as_a_reviewer,
         name='apply_as_a_reviewer'),
    path('<str:conf_name>/make_review/<str:title>',
         views.make_review, name='make_review'),
    path('<str:conf_name>/edit_review/<str:title>',
         views.edit_review, name='edit_review'),
]
