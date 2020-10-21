from django.shortcuts import render
import requests
from geopy.geocoders import Nominatim
from .forms import CityForm
from .models import City
from django.views.generic import DeleteView, TemplateView
from django.urls import reverse_lazy
import datetime


class IndexView(TemplateView):
    template_name = 'Base.html'


def Current(request):
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
            'x-rapidapi-key': "6446924734mshd20c29c9014fd63p155d13jsnc1cdd0345c05"
        }
        # Get all the features of this particular city, in the last 24 hours
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()

        # Get only the current features of this particular city and put it in a dictionary
        City_Weather = {
            'Id': city.Id,
            'City': city.Address,
            'Date': datetime.datetime.fromtimestamp(data['current']['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'Temperature': data['current']['temp'],
            'Humidity': data['current']['humidity'],
            'Wind_Speed': data['current']['wind_speed'],
            'Pressure': data['current']['pressure'],
            'Icon': data['current']['weather'][0]['icon'],
        }

        Weather_list.append(City_Weather)
    context = {'Weather_list': Weather_list, 'form': form}

    return render(request, 'WeatherApp/Current_Weather.html', context)


class WeatherDeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_confirm_delete.html"
    success_url = reverse_lazy("WeatherApp:current")


def Hourly(request):
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"
    url_second = "https://community-open-weather-map.p.rapidapi.com/weather"
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)  # Handling form request

        if form.is_valid():
            New_City = form.cleaned_data['Address']
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
    Weather_Dict = {}
    Weather_city = []

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
            'x-rapidapi-key': "6446924734mshd20c29c9014fd63p155d13jsnc1cdd0345c05"
        }
        # Get all the features of this particular city, in the last 24 hours
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        # Get only the hourlies features of this particular city and put it in a dictionary

        hourly = data['hourly']
        i = 0
        for i in range(0, 24):
            Weather_Dict["Horario{}".format(i)] = datetime.datetime.fromtimestamp(hourly[i]['dt']).strftime('%Y-%m-%d %H:%M:%S')
            Weather_Dict["Temperature{}".format(i)] = hourly[i]['temp']
            Weather_Dict["Humidity{}".format(i)] = hourly[i]['humidity']
            Weather_Dict["Wind_speed{}".format(i)] = hourly[i]['wind_speed']
            Weather_Dict["Pressure{}".format(i)] = hourly[i]['pressure']
            Weather_Dict["Icon{}".format(i)] = hourly[i]['weather'][0]['icon']
            i += 1

        Weather_Dict["Address"] = city.Address
        Weather_Dict["Id"] = city.Id
        print(Weather_Dict)
        Weather_city.append(Weather_Dict)

    context = {'Weather_city': Weather_city, 'form': form}

    return render(request, 'WeatherApp/Hourly_Weather.html', context)


class WeatherHourlyDeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_hourly_confirm_delete.html"
    success_url = reverse_lazy("WeatherApp:hourly")