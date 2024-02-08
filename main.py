import sys
import pygame
from pygame.locals import *
from io import BytesIO
import requests

# toponym_to_find = " ".join(sys.argv[1:])
toponym_to_find = 'спб'

# geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
#
# geocoder_params = {
#     "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
#     "geocode": toponym_to_find,
#     "format": "json"}
#
# response = requests.get(geocoder_api_server, params=geocoder_params)
#
# if not response:
#     pass
#
# json_response = response.json()
# toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# toponym_coodrinates = toponym["Point"]["pos"]
# toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = 0.005

# map_params = {
#     "ll": ",".join([toponym_longitude, toponym_lattitude]),
#     "spn": ",".join([str(delta), str(delta)]),
#     "l": "map"
# }

map_api_server = "http://static-maps.yandex.ru/1.x/"

# response = requests.get(map_api_server, params=map_params)

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
# Game loop.
while True:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([str(delta), str(delta)]),
            "l": "map"
        }
    response = requests.get(map_api_server, params=map_params)
    map_image = pygame.image.load(BytesIO(response.content))
    map_image = pygame.transform.scale(map_image, (550, 550))
    screen.fill((0, 0, 0))
    screen.blit(map_image, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if delta >= 0.01:
                    delta -= delta / 2
            if event.key == pygame.K_PAGEDOWN:
                if delta < 81.92:
                    delta += delta

    # Update.

    # Draw.

    pygame.display.flip()
    fpsClock.tick(fps)