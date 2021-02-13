# -*- coding: utf-8 -*-
import math
import sys
from io import BytesIO
import requests
from PIL import Image


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def spn_counter(coords):
    if len(coords) >= 2:
        coords = [[float(coord[0]), float(coord[1])] for coord in coords]
        point_a = coords[0]
        min_long = 0
        min_index = 1
        for i, point_b in enumerate(coords):
            long = lonlat_distance(point_a, point_b)
            if long > min_long:
                min_long = long
                min_index = i
        spn = max(round(abs(float(point_a[1]) - float(coords[min_index][1])), 6),
                  round(abs(float(point_a[0]) - float(coords[min_index][0])), 6))
        return spn, spn
    return 0.2, 0.2


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
toponym_longitude_start, toponym_lattitude_start = toponym_coodrinates_start.split(" ")

# поиск аптеки
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = ",".join([toponym_longitude_start, toponym_lattitude_start])
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    sys.exit(1)
json_response = response.json()
# Получаем первую найденную организацию.
organizations = json_response["features"][:12]

ll = ",".join(map(str, toponym_coodrinates_start.split(" ")))
spn = ",".join(map(str, spn_counter([toponym_coodrinates_start.split(" ")] +
                                    [org['geometry']['coordinates'] for org in organizations])))
pt = list()
for i, org in enumerate(organizations):
    hours = org["properties"]["CompanyMetaData"]["Hours"]["Availabilities"][0]
    color = "bl"
    if any("TwentyFourHours" in key for key in hours.keys()):
        color = "gn"
    elif len(hours.keys()) == 0:
        color = "gr"
    pt.append(f"{','.join(map(str, org['geometry']['coordinates']))},pm2{color}m{i + 1}")

map_params = {
    "ll": ll,
    "spn": spn,
    "l": "map",
    "pt": "~".join(pt)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
