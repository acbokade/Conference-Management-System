from django.urls import path
from . import views

urlpatterns = [
    path('apply_as_a_reviewer', views.apply_as_a_reviewer,
         name='apply_as_a_reviewer'),
    path('make_review', views.make_review, name='make_review'),
    path('edit_review',
         views.edit_review, name='edit_review'),
]
