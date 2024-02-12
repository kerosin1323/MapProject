import os
import sys

import pygame
import requests

coord = input('Введите координаты: ')
spn = int(input('Введите масштаб: '))
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord}&z={spn}&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл
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
                print(coord, spn)
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