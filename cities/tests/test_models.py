from decimal import InvalidOperation

from django.db.utils import IntegrityError
from django.test import TestCase

from cities.models import City


class CityModelTestCase(TestCase):
    def create_city(self, name, latitude, longitude):
        return City.objects.create(name=name, latitude=latitude, longitude=longitude)

    def test_correct_city(self):
        city = self.create_city("Belgorod", 50.5955595, 36.5873394)

        self.assertEqual(city.name, "Belgorod")
        self.assertEqual(city.latitude, 50.5955595)
        self.assertEqual(city.longitude, 36.5873394)

    def test_string_representation(self):
        city = self.create_city("Belgorod", 50.5955595, 36.5873394)
        self.assertEqual(str(city), "Belgorod city")

    def test_non_unique_city_name(self):
        self.create_city("Belgorod", 50.5955595, 36.5873394)
        self.assertRaises(
            IntegrityError,
            self.create_city,
            name="Belgorod",
            latitude=50.5955595,
            longitude=36.5873394,
        )

    def test_empty_city_name(self):
        self.assertRaises(
            IntegrityError,
            self.create_city,
            name=None,
            latitude=50.5955595,
            longitude=36.5873394,
        )

    def test_invalid_latitude(self):
        self.assertRaises(
            InvalidOperation,
            self.create_city,
            name="London",
            latitude=2222,
            longitude=80.9993321,
        )

    def test_invalid_longitude(self):
        self.assertRaises(
            InvalidOperation,
            self.create_city,
            name="Moscow",
            latitude=58.6612994,
            longitude=8000,
        )
