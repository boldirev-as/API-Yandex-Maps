import os
import random
import sys

import pygame
import requests


def get_size_toponym(toponym, static=True):
    if static:
        toponym_upper_lower = toponym["boundedBy"]["Envelope"]
        toponym_upper, toponym_lower = toponym_upper_lower["lowerCorner"].split(" ")
        toponym_upper_2, toponym_lower_2 = toponym_upper_lower["upperCorner"].split(" ")
    else:
        pass

    delta_1 = round(abs(float(toponym_lower) - float(toponym_lower_2)) / 2, 6)
    delta_2 = round(abs(float(toponym_upper) - float(toponym_upper_2)) / 2, 6)
    return delta_1, delta_2


cities = ["Ekb", "Msk", "Oslo", "Budapest", "Tomsk"]
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"

maps = []
for i, city in enumerate(cities):
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym_start = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates_start = toponym_start["Point"]["pos"]
    long, latt = toponym_coodrinates_start.split(" ")
    size_toponym = get_size_toponym(toponym_start)

    long = float(long) - random.randint(0, 100) * 0.001 * size_toponym[0]
    latt = float(latt) - random.randint(0, 100) * 0.001 * size_toponym[1]

    map_params = {
        "ll": ",".join(map(str, (long, latt))),
        "spn": ",".join(map(lambda x: str(x * 0.01), size_toponym)),
        "l": "map" if random.randint(0, 1) else "sat"
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = f"map{i}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    maps.append(map_file)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

running = True
fps = 1
clock = pygame.time.Clock()
count = 0

while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(pygame.image.load(maps[count]), (0, 0))

    count = (count + 1) % len(maps)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# Удаляем за собой файл с изображением.
[os.remove(map_file) for map_file in maps]
