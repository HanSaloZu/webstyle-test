from django.test import TestCase
from rest_framework.exceptions import APIException

from cities.models import City
from cities.services import (create_city, find_closest_city,
                             find_n_closest_cities, get_city_geodata)
from utils.tests import SleepyTestCase


class FindClosestCityTestCase(TestCase):
    def test_find_closest_of_three_cities(self):
        create_city("Moscow", 55.7504461, 37.6174943)
        create_city("London", 51.5073219, -0.1276474)
        create_city("Belgorod", 50.5955595, 36.5873394)

        closest_city = find_closest_city(City.objects.all(), latitude=50, longitude=0)

        self.assertEqual(closest_city.name, "London")

    def test_find_closest_of_none_city(self):
        closest_city = find_closest_city(City.objects.all(), latitude=50, longitude=0)

        self.assertIsNone(closest_city)


class FindNClosestCitiesTestCase(TestCase):
    def test_find_two_closest_of_three_cities(self):
        moscow = create_city("Moscow", 55.7504461, 37.6174943)
        london = create_city("London", 51.5073219, -0.1276474)
        create_city("Tokyo", 35.6828387, 139.7594549)

        closest_cities = find_n_closest_cities(
            2, City.objects.all(), latitude=50, longitude=0
        )

        self.assertIn(moscow, closest_cities)
        self.assertIn(london, closest_cities)
        self.assertEqual(len(closest_cities), 2)

    def test_find_two_closest_of_none_city(self):
        closest_cities = find_n_closest_cities(
            2, City.objects.all(), latitude=50, longitude=0
        )

        self.assertEqual(len(closest_cities), 0)

    def test_find_two_closest_of_one_city(self):
        create_city("London", 51.5073219, -0.1276474)
        closest_cities = find_n_closest_cities(
            2, City.objects.all(), latitude=50, longitude=0
        )

        self.assertEqual(len(closest_cities), 1)
        self.assertEqual(closest_cities[0].name, "London")

    def test_find_two_closest_of_two_cities(self):
        moscow = create_city("Moscow", 55.7504461, 37.6174943)
        tokyo = create_city("Tokyo", 35.6828387, 139.7594549)
        closest_cities = find_n_closest_cities(
            2, City.objects.all(), latitude=50, longitude=0
        )

        self.assertEqual(len(closest_cities), 2)
        self.assertIn(moscow, closest_cities)
        self.assertIn(tokyo, closest_cities)


class GetCityGeodataTestCase(SleepyTestCase):
    def test_get_geodata_with_correct_city_name(self):
        geodata = get_city_geodata("Moscow")

        self.assertIn("name", geodata)
        self.assertIn("latitude", geodata)
        self.assertIn("longitude", geodata)
        self.assertEqual(len(geodata), 3)
        self.assertEqual(geodata["name"], "Moscow")

    def test_get_geodata_with_incorrect_city_name(self):
        try:
            get_city_geodata("Amogus")
            self.fail("APIException not raised by get_city_geodata")
        except APIException as e:
            self.assertEqual(e.detail, "Unable to geocode")
