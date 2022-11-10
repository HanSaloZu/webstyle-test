from django.urls import include, path
from rest_framework import routers

from cities.views import CityViewSet, ClosestCitiesView

router = routers.SimpleRouter()
router.register(r"cities", CityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("closest/", ClosestCitiesView.as_view(), name="closest-cities"),
]
