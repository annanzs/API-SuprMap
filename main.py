import sys
import pygame
from pygame.locals import *
from io import BytesIO
import requests

pygame.font.init()

toponym_to_find = 'россия'

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(250, 50, 250, 42)
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

delta = 0.005

l = 'map'

map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([str(delta), str(delta)]),
    "l": l
}
response = requests.get(map_api_server, params=map_params)

search_image = pygame.image.load('magnifying.png')
search_image = pygame.transform.scale(search_image, (75, 75))
search_image_rect = pygame.Rect((500, 25), (75, 75))
map_image = pygame.image.load(BytesIO(response.content))
map_icon = pygame.image.load('map.png')
map_icon = pygame.transform.scale(map_icon, (75, 75))

sat_icon = pygame.image.load('sat.jpg')
sat_icon = pygame.transform.scale(sat_icon, (75, 75))

gib_icon = pygame.image.load('gibrid.jpg')
gib_icon = pygame.transform.scale(gib_icon, (75, 75))

map_icon_rect = pygame.Rect((650, 262), (75, 75))
sat_icon_rect = pygame.Rect((650, 362), (75, 75))
gib_icon_rect = pygame.Rect((650, 462), (75, 75))
# Game loop.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
                color = color_active if active else color_inactive
            else:
                active = False
                color = color_active if active else color_inactive

            if search_image_rect.collidepoint(event.pos) and text:
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
                try:
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                except:
                    pass
                toponym_coodrinates = toponym["Point"]["pos"]
                toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
                text = ''

            if map_icon_rect.collidepoint(event.pos):
                l = 'map'

            if sat_icon_rect.collidepoint(event.pos):
                l = 'sat'

            if gib_icon_rect.collidepoint(event.pos):
                l = 'sat,skl'

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_PAGEUP:
                if delta >= 0.01:
                    delta -= delta / 2
            if event.key == pygame.K_PAGEDOWN:
                if delta < 81.92:
                    delta += delta
            if event.key == pygame.K_UP and float(toponym_lattitude) < 85:
                toponym_lattitude = str(float(toponym_lattitude) + delta)
            if event.key == pygame.K_DOWN and float(toponym_lattitude) > -85:
                toponym_lattitude = str(float(toponym_lattitude) - delta)
            if event.key == pygame.K_RIGHT and float(toponym_longitude) < 85:
                toponym_longitude = str(float(toponym_longitude) + delta)
            if event.key == pygame.K_LEFT and float(toponym_longitude) > -85:
                toponym_longitude = str(float(toponym_longitude) - delta)

    # Update.
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([str(delta), str(delta)]),
        "l": l
    }
    response = requests.get(map_api_server, params=map_params)
    map_image = pygame.image.load(BytesIO(response.content))
    map_image = pygame.transform.scale(map_image, (500, 500))

    # Draw.
    screen.fill((205, 92, 92))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(map_image, (100, 150))
    screen.blit(search_image, search_image_rect)
    screen.blit(map_icon, map_icon_rect)
    screen.blit(sat_icon, sat_icon_rect)
    screen.blit(gib_icon, gib_icon_rect)

    pygame.display.flip()
    fpsClock.tick(fps)
