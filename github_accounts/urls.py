from . import views
from django.urls import path

urlpatterns = [
   path('', views.home, name="home"),
   path('user/', views.user, name="user"),
   path('weather/', views.weather, name="weather"),
   path('weather/delete/<city_name>/', views.delete_city, name="delete_city"),
]