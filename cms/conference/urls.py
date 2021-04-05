from django.urls import path
from . import views

urlpatterns = [
    path('create_conference', views.create_conference, name='create_conference'),
    path('update_conference', views.update_conference, name='update_conference'),
    path('create_workshop', views.create_workshop, name='create_workshop')
]