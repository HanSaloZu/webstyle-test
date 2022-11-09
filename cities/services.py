from math import dist

from cities.models import City


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
