import os
import sys

import pygame
import requests

spn_to_px_convert = {1: 0, 2: 0, 3: 0.5, 4: 0.5, 5: 0.1, 6: 0.1, 7: 0.08, 8: 0.08, 9: 0.06, 10: 0.04, 11: 0.04}
coord = input('Введите координаты: ')
spn = input('Введите масштаб: ')
coord_list = coord.split(',')
coord_list[0] = float(coord_list[0])
coord_list[1] = float(coord_list[1])
coord = str(coord_list[1]) + "," + str(coord_list[0])
if int(spn) < 6:
    zoom = 0.001
elif 5 < int(spn) < 12:
    zoom = 0.007
else:
    zoom = 0.01

map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
work = True
while work:  # цикл работы карты
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
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                    response = requests.get(map_request)  # создание нового запроса
                    if not response:  # проверка на ошибки
                        pygame.quit()
                        work = False
                        print("Ошибка выполнения запроса:")
                        print(map_request)
                        print("Http статус:", response.status_code, "(", response.reason, ")")
                        sys.exit(1)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                    pygame.display.flip()
                    os.remove(map_file)  # удаление фото после вывода, для экономии памяти

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
                    map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                    response = requests.get(map_request)  # создание нового запроса
                    if not response:  # проверка на ошибки
                        pygame.quit()
                        work = False
                        print("Ошибка выполнения запроса:")
                        print(map_request)
                        print("Http статус:", response.status_code, "(", response.reason, ")")
                        sys.exit(1)
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                    pygame.display.flip()
                    os.remove(map_file)  # удаление фото после вывода, для экономии памяти

            if event.key == pygame.K_DOWN:  # движение вниз
                if coord_list[0] - zoom > -90:  # границы движения
                    coord_list[0] -= zoom
                    coord = str(coord_list[1]) + "," + str(coord_list[0])
                map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                response = requests.get(map_request)  # создание нового запроса
                if not response:  # проверка на ошибки
                    pygame.quit()
                    work = False
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                pygame.display.flip()
                os.remove(map_file)  # удаление фото после вывода, для экономии памяти

            if event.key == pygame.K_UP:  # движение вверх
                if coord_list[0] + zoom < 90:  # границы движения
                    coord_list[0] += zoom
                    coord = str(coord_list[1]) + "," + str(coord_list[0])
                map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                response = requests.get(map_request)  # создание нового запроса
                if not response:  # проверка на ошибки
                    pygame.quit()
                    work = False
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                pygame.display.flip()
                os.remove(map_file)  # удаление фото после вывода, для экономии памяти

            if event.key == pygame.K_RIGHT:  # движение вправо
                if coord_list[1] + zoom < 180:  # границы движения
                    coord_list[1] += zoom
                    coord = str(coord_list[1]) + "," + str(coord_list[0])
                map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                response = requests.get(map_request)  # создание нового запроса
                if not response:  # проверка на ошибки
                    pygame.quit()
                    work = False
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                pygame.display.flip()
                os.remove(map_file)  # удаление фото после вывода, для экономии памяти

            if event.key == pygame.K_LEFT:  # движение влево
                if coord_list[1] - zoom > -180:  # границы движения
                    coord_list[1] -= zoom
                    coord = str(coord_list[1]) + "," + str(coord_list[0])
                map_request = f"http://static-maps.yandex.ru/1.x/?ll={''.join(coord)}&z={spn}&l=map"
                response = requests.get(map_request)  # создание нового запроса
                if not response:  # проверка на ошибки
                    pygame.quit()
                    work = False
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))  # вывод нового фрагмента карты на экран
                pygame.display.flip()
                os.remove(map_file)  # удаление фото после вывода, для экономии памяти



# Удаляем за собой файл с изображением.
os.remove(map_file)
