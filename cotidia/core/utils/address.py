import json

from raven.contrib.django.raven_compat.models import client
from urllib.request import urlopen
from urllib.parse import urlencode

from django.conf import settings


def geolocate(address):
    geolocated = False
    lat, lng = None, None

    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {"address": address, "key": settings.GOOGLE_API_KEY}
    url = "{}?{}".format(endpoint, urlencode(payload))

    try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)
        geolocation = data["results"][0]["geometry"]["location"]
        lat = geolocation["lat"]
        lng = geolocation["lng"]
        geolocated = True
    except Exception:
        client.captureException()

    return geolocated, lat, lng
