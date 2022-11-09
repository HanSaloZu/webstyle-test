from decouple import config
from requests.exceptions import HTTPError

from cities.geocoder import Geocoder
from utils.tests import SleepyTestCase


class GeocoderTestCase(SleepyTestCase):
    def test_incorrect_city_name(self):
        geocoder = Geocoder(config("API_KEY"))

        try:
            geocoder.geocode_city("Amogus")
            self.fail("HTTPError not raised by geocode_city")
        except HTTPError as e:
            self.assertEqual(e.response.status_code, 404)
            self.assertEqual(e.response.json()["error"], "Unable to geocode")

    def test_correct_city_name(self):
        geocoder = Geocoder(config("API_KEY"))
        response = geocoder.geocode_city("Belgorod")

        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["type"], "city")
        self.assertIn("lat", response[0])
        self.assertIn("lon", response[0])
        self.assertEqual(response[0]["address"]["city"], "Belgorod")

    def test_invalid_api_key(self):
        geocoder = Geocoder("invalid api key")

        try:
            geocoder.geocode_city("London")
            self.fail("HTTPError not raised by geocode_city")
        except HTTPError as e:
            self.assertEqual(e.response.status_code, 401)
            self.assertEqual(e.response.json()["error"], "Invalid key")
