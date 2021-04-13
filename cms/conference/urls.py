from django.urls import path
from . import views

urlpatterns = [
    path('list_conferences', views.list_conferences, name='list_conferences'),
    path('create_conference', views.create_conference, name='create_conference'),
    path('update_conference/<str:name>',
         views.update_conference, name='update_conference'),
    path('create_workshop', views.create_workshop, name='create_workshop'),
    path('update_workshop/<str:name>',
         views.update_conference, name='update_workshop'),
]
