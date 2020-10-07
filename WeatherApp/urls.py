from django.urls import path
from . import views

app_name = 'WeatherApp'

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<city_name>/', views.WeatherDeleteView.as_view(), name='delete_city')
]