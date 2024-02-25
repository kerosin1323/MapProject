import os
from functions import *
import pygame

spn_to_px_convert = {1: 0, 2: 0, 3: 0.5, 4: 0.5, 5: 0.1, 6: 0.1, 7: 0.08, 8: 0.08, 9: 0.06, 10: 0.04, 11: 0.04}
spn = 10
zoom = 0.007
l = 'map'

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.fill((0, 0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
work = False
text = ''


class Search:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        self.text_input_box = TextInputBox(50, 200, 500, font, self.func)
        group = pygame.sprite.Group(self.text_input_box)
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
            group.update(event_list)
            # заголовок
            self.textSurface = font.render('Введите объект: ', True, (255, 255, 255), None)
            self.textRect = self.textSurface.get_rect(center=(300, 175))
            self.screen.blit(self.textSurface, self.textRect)
            group.draw(screen)
            pygame.display.flip()

    def func(self):
        global work, text
        work = True
        text = self.text_input_box.text
        self.running = False


searching = Search(screen)
searching.update()
geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text}&format=json"
geocoder_response = requests.get(geocoder_request).json()["response"]["GeoObjectCollection"]["featureMember"][0][
    "GeoObject"]
coord = geocoder_response["Point"]["pos"].split()
coord_list = list(map(float, geocoder_response["Point"]["pos"].split()))
pt = f"{','.join(coord)},round"
map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(coord)}&z={spn}&l={l}&pt={pt}"
map_file = get_response(map_request)[0]

while work:
    screen.blit(pygame.image.load(map_file), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # выход с проги
            pygame.quit()
            work = False
        if event.type == pygame.KEYDOWN:  # отслеживание клавиш pg_up и pg_down
            if event.key == pygame.K_PAGEUP:  # увеличение
                if int(spn) + 1 < 20:  # границы увеличения
                    spn = int(spn) + 1
                    print(spn)
                    if 4 < int(spn) < 6:
                        zoom = 0.5
                        print(zoom)
                    elif 11 < int(spn) < 15:
                        zoom = 0.003
                        print(zoom)
                    elif 9 < int(spn) < 12:
                        zoom = 0.007
                        print(zoom)
                    elif 8 < int(spn) < 10:
                        zoom = 0.07
                        print(zoom)
                    elif 5 < int(spn) < 9:
                        zoom = 0.1
                        print(zoom)
                    elif int(spn) < 5:
                        zoom = 0.8
                        print(zoom)
                    elif 14 < int(spn) < 18:
                        zoom = 0.0005
                        print(zoom)
                    else:
                        zoom = 0.001
                        print(zoom)

            if event.key == pygame.K_PAGEDOWN:  # уменьшение
                if int(spn) - 1 > 0:  # границы уменьшения
                    spn = int(spn) - 1
                    print(spn)
                    if 4 < int(spn) < 6:
                        zoom = 0.5
                        print(zoom)
                    elif 11 < int(spn) < 15:
                        zoom = 0.003
                        print(zoom)
                    elif 9 < int(spn) < 12:
                        zoom = 0.007
                        print(zoom)
                    elif 8 < int(spn) < 10:
                        zoom = 0.07
                        print(zoom)
                    elif 5 < int(spn) < 9:
                        zoom = 0.1
                        print(zoom)
                    elif int(spn) < 5:
                        zoom = 0.8
                        print(zoom)
                    elif 14 < int(spn) < 18:
                        zoom = 0.0005
                        print(zoom)
                    else:
                        zoom = 0.001
                        print(zoom)

            if event.key == pygame.K_DOWN:  # движение вниз
                if coord_list[1] - zoom > -90:  # границы движения
                    coord_list[1] -= zoom

            if event.key == pygame.K_UP:  # движение вверх
                if coord_list[1] + zoom < 90:  # границы движения
                    coord_list[1] += zoom

            if event.key == pygame.K_RIGHT:  # движение вправо
                if coord_list[0] + zoom < 180:  # границы движения
                    coord_list[0] += zoom

            if event.key == pygame.K_LEFT:  # движение влево
                if coord_list[0] - zoom > -180:  # границы движения
                    coord_list[0] -= zoom

            if event.key == pygame.K_1:
                l = "sat"

            if event.key == pygame.K_2:
                l = 'sat,skl'

            if event.key == pygame.K_3:
                l = 'map'

        coord = [str(coord_list[0]), str(coord_list[1])]
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(coord)}&z={spn}&l={l}&pt={pt}"
        map_file, work = get_response(map_request)
        screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
        pygame.display.flip()

