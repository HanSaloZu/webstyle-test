from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from cities.services import create_city


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
