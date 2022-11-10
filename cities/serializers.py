from rest_framework import serializers


class CoordinatesSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, max_value=90, min_value=-90
    )
    longitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, max_value=180, min_value=-180
    )

    class Meta:
        fields = ("latitude", "longitude")
