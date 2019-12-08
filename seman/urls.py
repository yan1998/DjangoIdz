from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_file/', views.add_file, name='add_file'),
]
