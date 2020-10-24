from django.urls import path
from . import views

app_name = 'WeatherApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('current', views.Current, name='current'),
    path('delete/<pk>/', views.WeatherDeleteView.as_view(), name='delete_city'),
    path('hourly', views.Hourly, name='hourly'),
    path('delete_hourly/<pk>/', views.WeatherHourlyDeleteView.as_view(), name='delete_hourly_city'),
    path('average', views.Average, name='average'),
    path('delete_average/<pk>/', views.WeatherAverageDeleteView.as_view(), name='delete_average_city'),
]