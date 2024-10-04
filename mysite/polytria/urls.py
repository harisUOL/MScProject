from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='polytria-home'),
    path('regularise_and_triangulate/', views.regularise_and_triangulate, name='polytria-regularise_and_triangulate'),
    path('about/', views.about, name='polytria-about'),
] 