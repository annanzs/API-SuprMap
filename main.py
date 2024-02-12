import sys
import pygame
from pygame.locals import *
from io import BytesIO
import requests

pygame.font.init()

toponym_to_find = 'спб'

delta = 0.005

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect(100, 100, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

map_api_server = "http://static-maps.yandex.ru/1.x/"

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

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
map_image = pygame.transform.scale(map_image, (500, 500))
# Game loop.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    active = False
                    color = color_active if active else color_inactive
                    toponym_to_find = text
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
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_PAGEUP:
                if delta >= 0.01:
                    delta -= delta / 2
            if event.key == pygame.K_PAGEDOWN:
                if delta < 81.92:
                    delta += delta

    # Update.
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": "map"
    }
    response = requests.get(map_api_server, params=map_params)
    map_image = pygame.image.load(BytesIO(response.content))
    map_image = pygame.transform.scale(map_image, (500, 500))

    # Draw.
    screen.fill((0, 0, 0))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(map_image, (0, 150))

    pygame.display.flip()
    fpsClock.tick(fps)
