from cities.models import City


def create_city(name, latitude, longitude):
    return City.objects.create(name=name, latitude=latitude, longitude=longitude)
