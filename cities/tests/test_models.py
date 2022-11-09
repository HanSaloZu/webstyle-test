from decimal import InvalidOperation

from django.db.utils import IntegrityError
from django.test import TestCase

from cities.services import create_city


class CityModelTestCase(TestCase):
    def test_correct_city(self):
        city = create_city("Belgorod", 50.5955595, 36.5873394)

        self.assertEqual(city.name, "Belgorod")
        self.assertEqual(city.latitude, 50.5955595)
        self.assertEqual(city.longitude, 36.5873394)

    def test_string_representation(self):
        city = create_city("Belgorod", 50.5955595, 36.5873394)
        self.assertEqual(str(city), "Belgorod city")

    def test_non_unique_city_name(self):
        create_city("Belgorod", 50.5955595, 36.5873394)
        self.assertRaises(
            IntegrityError,
            create_city,
            name="Belgorod",
            latitude=50.5955595,
            longitude=36.5873394,
        )

    def test_empty_city_name(self):
        self.assertRaises(
            IntegrityError,
            create_city,
            name=None,
            latitude=50.5955595,
            longitude=36.5873394,
        )

    def test_invalid_latitude(self):
        self.assertRaises(
            InvalidOperation,
            create_city,
            name="London",
            latitude=2222,
            longitude=80.9993321,
        )

    def test_invalid_longitude(self):
        self.assertRaises(
            InvalidOperation,
            create_city,
            name="Moscow",
            latitude=58.6612994,
            longitude=8000,
        )
