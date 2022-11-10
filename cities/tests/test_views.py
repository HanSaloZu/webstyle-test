from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from cities.models import City
from cities.services import create_city
from utils.tests import SleepyTestCase


class CityViewSetTestCase(SleepyTestCase):
    def test_create_city(self):
        payload = {"name": "Moscow"}
        response = self.client.post(reverse("city-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["name"], "Moscow")

    def test_create_city_with_invalid_data(self):
        payload = {"name": ""}
        response = self.client.post(reverse("city-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_city(self):
        url = reverse(
            "city-detail",
            args=[1],
        )
        create_city("London", 51.5073219, -0.1276474)
        self.assertEqual(City.objects.all().count(), 1)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(City.objects.all().count(), 0)

    def test_city_detail(self):
        url = reverse(
            "city-detail",
            args=[1],
        )
        create_city("London", 51.5073219, -0.1276474)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["name"], "London")
        self.assertIn("latitude", response.data)
        self.assertIn("longitude", response.data)

    def test_nonexistent_city_detail(self):
        url = reverse(
            "city-detail",
            args=[35],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_cities_list(self):
        create_city("Moscow", 55.7504461, 37.6174943)
        create_city("London", 51.5073219, -0.1276474)
        create_city("Belgorod", 50.5955595, 36.5873394)

        response = self.client.get(reverse("city-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["count"], 3)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertIn("id", response.data["results"][0])
        self.assertIn("name", response.data["results"][0])
        self.assertIn("latitude", response.data["results"][0])
        self.assertIn("longitude", response.data["results"][0])


class ClosestCitiesViewTestCase(TestCase):
    url = reverse("closest-cities")

    def test_request_closest_of_three_cities(self):
        create_city("Moscow", 55.7504461, 37.6174943)
        create_city("London", 51.5073219, -0.1276474)
        create_city("Belgorod", 50.5955595, 36.5873394)

        payload = {"latitude": "50", "longitude": "0"}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertIn("id", response.data[0])
        self.assertIn("name", response.data[0])
        self.assertIn("latitude", response.data[0])
        self.assertIn("longitude", response.data[0])

    def test_request_closest_of_none_city(self):
        payload = {"latitude": "50", "longitude": "0"}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_invalid_request(self):
        payload = {"latitude": "5000"}
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
