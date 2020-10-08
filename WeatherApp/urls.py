from django.urls import path
from . import views

app_name = 'WeatherApp'

urlpatterns = [
    path('', views.index, name='home'),
    path('delete/<pk>/', views.WeatherDeleteView.as_view(), name='delete_city')
]