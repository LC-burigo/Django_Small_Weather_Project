from django.urls import path
from . import views

app_name = 'WeatherApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('current', views.Current, name='current'),
    path('delete_current/<pk>/', views.WeatherCurrentDeleteView.as_view(), name='delete_current_city'),
    path('hourly', views.Hourly, name='hourly'),
    path('delete_hourly/<pk>/', views.WeatherHourlyDeleteView.as_view(), name='delete_hourly_city'),
    path('average', views.Average, name='average'),
    path('delete_average/<pk>/', views.WeatherAverageDeleteView.as_view(), name='delete_average_city'),
    path('max_min', views.Max_Min, name='max_min'),
    path('delete_max_min/<pk>/', views.Weather_Max_Min_DeleteView.as_view(), name='delete_max_min_city'),
    path('grapics', views.Bar_Chart, name='graphics')
]