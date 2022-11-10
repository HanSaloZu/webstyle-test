from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cities.models import City
from cities.serializers import CitySerializer, CoordinatesSerializer
from cities.services import find_n_closest_cities


class CityViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = City.objects.all()
    lookup_field = "id"
    serializer_class = CitySerializer

    def get_queryset(self):
        return self.queryset.order_by("id")

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.extend_with_geodata()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ClosestCitiesView(APIView):
    queryset = City.objects.all()
    serializer_class = CoordinatesSerializer

    def post(self, request):
        coords_serializer = self.serializer_class(data=request.data)
        coords_serializer.is_valid(raise_exception=True)
        closest_cities = find_n_closest_cities(
            2,
            self.queryset,
            coords_serializer.validated_data["latitude"],
            coords_serializer.validated_data["longitude"],
        )
        city_serializer = CitySerializer(closest_cities, many=True)

        return Response(city_serializer.data, status=status.HTTP_200_OK)
