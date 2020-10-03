from django.shortcuts import render
import requests
from pprint import pprint
import datetime
from geopy.geocoders import Nominatim
from .forms import CityForm


def index(request):
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

        Geolocator = Nominatim(user_agent="Lucas")
        Location = Geolocator.geocode(city)
        Coordinates = []
        Latitude = Location.latitude
        Longitude = Location.longitude
        Coordinates.append(Latitude)
        Coordinates.append(Longitude)
        #############################################################################
        querystring = {"lat": Coordinates[0], "lon": Coordinates[1], "dt": timestamp}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "c9a626ea64msh6698ab14d44886ap1f605bjsn85a708b80b0f"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        city_weather = {
            'City': city,
            'Temperature': data['current']['temp'],
            'Humidity': data['current']['humidity'],
            'Wind_Speed': data['current']['wind_speed'],
            'Pressure': data['current']['pressure'],
        }
    context = {'city_weather': city_weather}
    return render(request, 'WeatherApp/Weather.html', context)
