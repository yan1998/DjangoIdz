from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.autorize, name='auth'),
    #path('seman', views.seman, name='seman'),
]
