from django.shortcuts import render
import urllib.request
import urllib.parse  # For space between city name such New Delhi
import json


def index(request):
    if request.method == "POST":
        city = request.POST["city"]
        api_key = "your api key"  # get your api key https://home.openweathermap.org/
        city_encoded = urllib.parse.quote(city)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}"

        try:
            source = urllib.request.urlopen(url).read()
            List_of_data = json.loads(source)
            temp_celsius = List_of_data["main"]["temp"] - 273.15

            data = {
                "country_code": str(List_of_data["sys"]["country"]),
                "coordinate": f'{List_of_data["coord"]["lon"]} {List_of_data["coord"]["lat"]}',
                "temp": f"{temp_celsius:.2f}°C",
                "pressure": str(List_of_data["main"]["pressure"]),
                "humidity": str(List_of_data["main"]["humidity"]),
            }
        except urllib.error.URLError as e:
            print(f"Error fetching data: {e}")
            data = {"error": "Error fetching data from the weather service."}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            data = {"error": "Error parsing weather data."}
        except KeyError as e:
            print(f"Missing data in response: {e}")
            data = {"error": "Incomplete weather data received."}
    else:
        data = {}

    return render(request, "main/index.html", data)
