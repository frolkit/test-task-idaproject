from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('image_create/', views.image_create, name='image_create'),
    path('image_edit/<int:id>/', views.image_edit, name='image_edit'),
]
