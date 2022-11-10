from rest_framework import serializers

from cities.models import City
from cities.services import create_city, get_city_geodata


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "latitude", "longitude")
        read_only_fields = ("id", "latitude", "longitude")

    def validate(self, data):
        if (
            self.geodata.get("name", None)
            and City.objects.filter(name__exact=self.geodata["name"]).exists()
        ):
            raise serializers.ValidationError(
                {"city": "city with this name already exists."}
            )

        return data

    def extend_with_geodata(self):
        self.geodata = get_city_geodata(self.initial_data.get("name", ""))

    def create(self, validated_data):
        validated_data.update(self.geodata)
        city = create_city(**validated_data)
        city.save()
        return city


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, max_value=90, min_value=-90
    )
    longitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, max_value=180, min_value=-180
    )

    class Meta:
        fields = ("latitude", "longitude")
