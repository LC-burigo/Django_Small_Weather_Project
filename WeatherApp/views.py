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
    Current_List = []

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
        Current_Dict = {
            'Id': city.Id,
            'City': city.Address,
            'Date': datetime.datetime.fromtimestamp(data['current']['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'Temperature': data['current']['temp'],
            'Humidity': data['current']['humidity'],
            'Wind_Speed': data['current']['wind_speed'],
            'Pressure': data['current']['pressure'],
            'Icon': data['current']['weather'][0]['icon'],
        }

        Current_List.append(Current_Dict)
    context = {'Current_List': Current_List, 'form': form}

    return render(request, 'WeatherApp/Current_Weather.html', context)


class WeatherCurrentDeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_current_confirm_delete.html"
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
    Hourly_Dict = {}
    Hourly_List = []

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
            Hourly_Dict["Horario{}".format(i)] = datetime.datetime.fromtimestamp(hourly[i]['dt']).strftime('%Y-%m-%d %H:%M:%S')
            Hourly_Dict["Temperature{}".format(i)] = hourly[i]['temp']
            Hourly_Dict["Humidity{}".format(i)] = hourly[i]['humidity']
            Hourly_Dict["Wind_speed{}".format(i)] = hourly[i]['wind_speed']
            Hourly_Dict["Pressure{}".format(i)] = hourly[i]['pressure']
            Hourly_Dict["Icon{}".format(i)] = hourly[i]['weather'][0]['icon']
            i += 1

        Hourly_Dict["Address"] = city.Address
        Hourly_Dict["Id"] = city.Id
        print(Hourly_Dict)
        Hourly_List.append(Hourly_Dict)

    context = {'Hourly_List': Hourly_List, 'form': form}

    return render(request, 'WeatherApp/Hourly_Weather.html', context)


class WeatherHourlyDeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_hourly_confirm_delete.html"
    success_url = reverse_lazy("WeatherApp:hourly")


def Average(request):
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

    Sum_Temperature = 0
    Sum_humidity = 0
    Sum_speedwind = 0
    Sum_pressure = 0
    Average_Dict = {}
    Average_List = []

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
        for i in range(0, 24):
            Sum_Temperature += hourly[i]['temp']
            Sum_humidity += hourly[i]['humidity']
            Sum_speedwind += hourly[i]['wind_speed']
            Sum_pressure += hourly[i]['pressure']

        Average_Dict = {
            "Temperature_average": Sum_Temperature/24,
            "Humidity_average": Sum_humidity/24,
            "WindSpeed_average": Sum_speedwind/24,
            "Pressure_average": Sum_pressure/24,
            "Id": city.Id,
            "Address": city.Address,
        }

        Average_List.append(Average_Dict)

    context = {'Average_List': Average_List, 'form': form}

    return render(request, 'WeatherApp/Average_Weather.html', context)


class WeatherAverageDeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_Average_confirm_delete.html"
    success_url = reverse_lazy("WeatherApp:average")


def Max_Min(request):
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

    List_Temperature = []
    List_humidity = []
    List_speedwind =[]
    List_pressure = []
    Max_Min_Dict = {}
    Max_Min_List = []

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
        for i in range(0, 24):
            List_Temperature.append(hourly[i]['temp'])
            List_humidity.append(hourly[i]['humidity'])
            List_speedwind.append(hourly[i]['wind_speed'])
            List_pressure.append(hourly[i]['pressure'])

        Max_Min_Dict = {
            "Max_Temperature": max(List_Temperature),
            "Min_Temperature": min(List_Temperature),
            "Max_Humidity": max(List_humidity),
            "Min_Humidity": min(List_humidity),
            "Max_WindSpeed": max(List_speedwind),
            "Min_WindSpeed": min(List_speedwind),
            "Max_Pressure": max(List_pressure),
            "Min_Pressure": min(List_pressure),
            "Id": city.Id,
            "Address": city.Address,
        }

        Max_Min_List.append(Max_Min_Dict)

    context = {'Max_Min_List': Max_Min_List, 'form': form}

    return render(request, 'WeatherApp/Max_Min_Weather.html', context)


class Weather_Max_Min_DeleteView(DeleteView):
    model = City
    context_object_name = "Wd"
    template_name = "WeatherApp/Weather_Max_Min_confirm_delete.html"
    success_url = reverse_lazy("WeatherApp:max_min")

