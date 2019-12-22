from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('sort_results/<command>/', views.sort_results, name='sort_results'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
