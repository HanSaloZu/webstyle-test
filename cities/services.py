from math import dist

from decouple import config
from requests.exceptions import RequestException
from rest_framework.exceptions import APIException

from cities.geocoder import Geocoder
from cities.models import City


def get_city_geodata(city_name):
    geocoder = Geocoder(config("API_KEY"))

    try:
        geodata = geocoder.geocode_city(city_name)[0]

        return {
            "name": geodata["address"]["city"],
            "latitude": geodata["lat"],
            "longitude": geodata["lon"],
        }
    except RequestException as e:
        raise APIException(e.response.json()["error"], e.response.status_code)
    except KeyError:
        raise APIException("Unable to geocode", 404)


def create_city(name, latitude, longitude):
    return City.objects.create(name=name, latitude=latitude, longitude=longitude)


def find_closest_city(cities, latitude, longitude):
    point_coords = (latitude, longitude)
    closest_city = None
    min_dist = float("inf")

    for city in cities:
        city_coords = (city.latitude, city.longitude)
        d = dist(city_coords, point_coords)
        if d < min_dist:
            min_dist = d
            closest_city = city

    return closest_city


def find_n_closest_cities(n, cities, latitude, longitude):
    closest_cities = []
    while n > 0 and cities.count() > 0:
        closest_cities.append(
            find_closest_city(
                cities.all(),
                latitude,
                longitude,
            )
        )
        cities = cities.all().exclude(name=closest_cities[-1].name)
        n -= 1

    return closest_cities
