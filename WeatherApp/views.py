from django.shortcuts import render
import requests
from pprint import pprint
import datetime
from geopy.geocoders import Nominatim
from .forms import CityForm
from .models import City


def index(request):
    Input_Address = 'london'
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"
    Cities = City.objects.all()
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)  # Handling form request
        form.save()

        # if form.is_valid():
        #     Address = form.cleaned_data['Address']

    Weather_list = []

    for city in Cities:

        # Get the coordinates of address of the city
        Geolocator = Nominatim(user_agent="Lucas")
        Location = Geolocator.geocode(city.Address)
        Coordinates = []
        Latitude = Location.latitude
        Longitude = Location.longitude
        Coordinates.append(Latitude)
        Coordinates.append(Longitude)
        #############################################################################
        querystring = {"lat": Coordinates[0], "lon": Coordinates[1], "dt": city.Dt}

        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "c9a626ea64msh6698ab14d44886ap1f605bjsn85a708b80b0f"
        }
        # Get all the features of this particular city, in the last 24 hours
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 200:

            data = response.json()

            # Get only the current features of this particular city and put it in a dictionary
            City_Weather = {
                'City': city.Address,
                'Temperature': data['current']['temp'],
                'Humidity': data['current']['humidity'],
                'Wind_Speed': data['current']['wind_speed'],
                'Pressure': data['current']['pressure'],
            }

            Weather_list.append(City_Weather)

        else:
            City_Weather = {}
            print('Address not found')

    context ={'Weather_list': Weather_list, 'form': form}

    return render(request, 'WeatherApp/Weather.html', context)
