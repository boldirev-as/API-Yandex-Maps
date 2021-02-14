import sys

import requests

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"
}

response = requests.get(geocoder_api_server, params=geocoder_params)

json_response = response.json()
toponym_start = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates_start = toponym_start["Point"]["pos"]

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_coodrinates_start.replace(" ", ","),
    "format": "json",
    "kind": "district"
}

response = requests.get(geocoder_api_server, params=geocoder_params)
toponym = response.json()
metadata = toponym["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]
district = metadata["GeocoderMetaData"]["text"]
print("->", district)
