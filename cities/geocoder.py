import requests


class Geocoder:
    __url = "https://eu1.locationiq.com/v1/search.php?"
    __params = {}

    def __init__(
        self, api_key, address_details=1, format="json", limit=1, accept_language="en"
    ):
        self.__params["key"] = api_key
        self.__params["format"] = format
        self.__params["limit"] = limit
        self.__params["addressdetails"] = address_details
        self.__params["accept-language"] = accept_language

    def geocode_city(self, city):
        params = {"city": city}
        params.update(self.__params)

        response = requests.get(self.__url, params)
        response.raise_for_status()
        return response.json()
