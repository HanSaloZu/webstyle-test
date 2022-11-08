from django.test import TestCase

from cities.models import City
from cities.services import find_closest_city


class FindClosestCityTestCase(TestCase):
    def create_city(self, name, latitude, longitude):
        return City.objects.create(name=name, latitude=latitude, longitude=longitude)

    def test_find_closest_of_three_cities(self):
        self.create_city("Moscow", 55.7504461, 37.6174943)
        self.create_city("London", 51.5073219, -0.1276474)
        self.create_city("Belgorod", 50.5955595, 36.5873394)

        closest_city = find_closest_city(City.objects.all(), latitude=50, longitude=0)

        self.assertEqual(closest_city.name, "London")

    def test_find_closest_of_none_city(self):
        closest_city = find_closest_city(City.objects.all(), latitude=50, longitude=0)

        self.assertIsNone(closest_city)
