from django.urls import path

from cities.views import ClosestCitiesView

urlpatterns = [
    path("closest/", ClosestCitiesView.as_view(), name="closest-cities"),
]
