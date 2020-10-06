from django.shortcuts import render
import requests
from pprint import pprint
import datetime
from geopy.geocoders import Nominatim
from .forms import CityForm
from .models import City


def index(request):
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"
    url_second = "https://community-open-weather-map.p.rapidapi.com/weather"
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)  # Handling form request

        if form.is_valid():
            New_City = form.cleaned_data['Address']
            New_Dt = form.cleaned_data['Dt']
            Existing_City = City.objects.filter(Address=New_City).count()
            if Existing_City == 0:
                querystring = {"callback": "test", "id": "2172797", "units": "%22metric%22 or %22imperial%22",
                               "mode": "xml%2C html", "q": New_City}

                headers = {
                    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
                    'x-rapidapi-key': "6446924734mshd20c29c9014fd63p155d13jsnc1cdd0345c05"
                }

                response = requests.request("GET", url_second, headers=headers, params=querystring)
                if response.status_code == 200:
                    form.save()
                else:
                    Error_message = 'City does not exist in the world'

            else:
                Error_message = 'City already exists in the database'



    Cities = City.objects.all()
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

        data = response.json()

        # Get only the current features of this particular city and put it in a dictionary
        City_Weather = {
            'City': city.Address,
            'Temperature': data['current']['temp'],
            'Humidity': data['current']['humidity'],
            'Wind_Speed': data['current']['wind_speed'],
            'Pressure': data['current']['pressure'],
            'Icon': data['current']['weather'][0]['icon'],
        }

        Weather_list.append(City_Weather)
        print(City_Weather['Icon'])
    context ={'Weather_list': Weather_list, 'form': form}

    return render(request, 'WeatherApp/Weather.html', context)
