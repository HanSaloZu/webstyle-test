from django.test import TestCase

from cities.serializers import CitySerializer, CoordinatesSerializer
from cities.services import create_city


class CitySerializerTestCase(TestCase):
    def test_serializer_with_instance(self):
        city = create_city("Berlin", 52.5170365, 13.3888599)
        serializer = CitySerializer(instance=city)
        data = serializer.data

        self.assertEqual(len(data), 4)
        self.assertEqual(data["id"], city.id)
        self.assertEqual(data["name"], city.name)
        self.assertEqual(data["latitude"], str(city.latitude))
        self.assertEqual(data["longitude"], str(city.longitude))


class CoordinatesSerializerTestCase(TestCase):
    def test_serializer_with_valid_data(self):
        data = {"latitude": "71.9621552", "longitude": "-10.9765338"}
        self.assertTrue(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_with_invalid_latitude(self):
        data = {"latitude": "1000", "longitude": "10.9765338"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_with_invalid_longitude(self):
        data = {"latitude": "1.9621552", "longitude": "-999"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_with_empty_latitude(self):
        data = {"latitude": "", "longitude": "-10.9765338"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

        data = {"latitude": None, "longitude": "-10.9765338"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_with_empty_longitude(self):
        data = {"latitude": "1.9621552", "longitude": ""}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

        data = {"latitude": "1.9621552", "longitude": None}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_without_latitude(self):
        data = {"longitude": "1.9621552"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_without_longitude(self):
        data = {"latitude": "1.9621552"}
        self.assertFalse(CoordinatesSerializer(data=data).is_valid())

    def test_serializer_without_data(self):
        self.assertFalse(CoordinatesSerializer(data={}).is_valid())
