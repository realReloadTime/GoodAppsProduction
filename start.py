# ЗАДАЧИ  !!!

# Нарисовать фоны для экранов, анимации(не в приоритете)
# Начать разработку дата базы для сохранения данных

import pygame
from win32api import GetSystemMetrics
import os
import sys


class SellAndGive:
    def __init__(self):
        # взять размеры экрана (нужно для правильного расположения объектов на любом экране)
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        self.menu_buttons = [['Новая игра', 0], ['Продолжить', 0], ['Авторы', 0],
                             ['Выйти', 0]]  # названия и состояния кнопок

        # расположение кнопок
        self.menu_button_location = []  # ЗАПИСЬ ПО СХЕМЕ
        # [x0 - обводка, y0 - обводка, ширина + обводка, высота + обводка]

        self.screen = pygame.display.set_mode((self.width, self.height))

        # менеджер экранов для удобного переключения между ними(список будет расширяться)
        self.all_screens = ['MainMenu', 'NewGameScreen', 'Continue', 'Authors', 'Desktop', 'Site']

        # отмечаем выбранный экран
        self.selected_screen = self.all_screens[0]
        self.start_plot_played = False

        # запускаем приложение
        self.app_running()

    def app_running(self):  # старт и работа приложения
        pygame.init()
        mouse_coords = (0, 0)

        pygame.display.set_caption('Продай и отдай')
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        running = True

        cursor = load_image('translucent_pixel.png', -1)
        cursor = pygame.transform.scale(cursor, (40, 50))

        while running:
            self.screen.fill((31, 204, 255))  # голубой цвет(заглушка для фона)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # выход на кнопку ESC
                    self.app_end()
                    running = False

                if event.type == pygame.MOUSEMOTION:
                    mouse_coords = event.pos

                    # ограничитель, исключает коллапс с другими экранами
                    if self.selected_screen == self.all_screens[0]:
                        for x, y, w, h in self.menu_button_location:
                            if x <= event.pos[0] <= x + w and y <= event.pos[1] <= y + h:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 1
                            else:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 0

                if event.type == pygame.MOUSEBUTTONDOWN:  # проверка нажатия мыши

                    if self.selected_screen == self.all_screens[0]:
                        # нажатие по кнопке выхода
                        if self.menu_button_location[3][0] <= event.pos[0] <=\
                                self.menu_button_location[3][0] + self.menu_button_location[3][2] and\
                                self.menu_button_location[3][1] <= event.pos[1] <=\
                                self.menu_button_location[3][1] + self.menu_button_location[3][3]:
                            self.app_end()
                            running = False
                        # нажатие по кнопке Новая Игра
                        elif self.menu_button_location[0][0] <= event.pos[0] <=\
                                self.menu_button_location[0][0] + self.menu_button_location[0][2] and\
                                self.menu_button_location[0][1] <= event.pos[1] <=\
                                self.menu_button_location[0][1] + self.menu_button_location[0][3]:
                            self.selected_screen = self.all_screens[1]
                        # нажатие по кнопке Продолжить
                        elif self.menu_button_location[1][0] <= event.pos[0] <=\
                                self.menu_button_location[1][0] + self.menu_button_location[1][2] and\
                                self.menu_button_location[1][1] <= event.pos[1] <=\
                                self.menu_button_location[1][1] + self.menu_button_location[1][3]:
                            self.selected_screen = self.all_screens[2]
                        # нажатие по кнопке Авторы
                        elif self.menu_button_location[2][0] <= event.pos[0] <=\
                                self.menu_button_location[2][0] + self.menu_button_location[2][2] and\
                                self.menu_button_location[2][1] <= event.pos[1] <=\
                                self.menu_button_location[2][1] + self.menu_button_location[2][3]:
                            self.selected_screen = self.all_screens[3]

            if not running:
                continue

            if self.selected_screen == 'MainMenu':  # действия при выборе экрана главного меню(по умолчанию)
                self.draw_main_menu()

            if self.selected_screen == 'NewGameScreen':
                if not self.start_plot_played:
                    self.start_plot()
                    self.start_plot_played = True

            if self.selected_screen == 'Desktop':
                pass

            if self.selected_screen == 'Site':
                pass

            self.screen.blit(cursor, mouse_coords)
            pygame.display.flip()
            clock.tick(100)

    def draw_main_menu(self):  # перенести сюда простыню из app_running
        menu_background = Background('data/background_menu.png', [0, 0])
        self.screen.blit(menu_background.image, menu_background.rect)

        for i in range(3):

            font = pygame.font.Font(None, 100)
            text = font.render(self.menu_buttons[i][0], True, pygame.Color('#FFE594'))  # текст
            text_x = self.width // 2 - text.get_width() // 2 - 50
            text_y = self.height // 3 - text.get_height() // 2 - 20 + i * 200
            text_w = text.get_width()
            text_h = text.get_height()
            if len(self.menu_button_location) != 4:  # избегаем перепись координат кнопок
                self.menu_button_location.append([text_x - 10, text_y - 10,
                                                  text_w + 20, text_h + 20])  # запись занимаемых координат кнопкой

            pygame.draw.rect(self.screen, (255, 150, 150), (text_x - 10, text_y - 10,
                                                            text_w + 20, text_h + 20), 0)  # фон текста
            if self.menu_buttons[i][1] == 0:
                pygame.draw.rect(self.screen, (10, 255, 0), (text_x - 10,
                                                             text_y - 10,
                                                             text_w + 20,
                                                             text_h + 20), 4)  # безфокусная обводка текста
            if self.menu_buttons[i][1] == 1:
                pygame.draw.rect(self.screen, (10, 0, 255), (text_x - 10,
                                                             text_y - 10,
                                                             text_w + 20,
                                                             text_h + 20), 4)  # фокусная обводка текста
            self.screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 100)
        text = font.render('Выход', True, (225, 225, 200))
        text_x = self.width - text.get_width() - 20
        text_y = self.height - text.get_height() - 20
        text_w = text.get_width()
        text_h = text.get_height()
        if len(self.menu_button_location) != 4:
            self.menu_button_location.append([text_x - 10, text_y - 10, text_w + 20, text_h + 20])
        if self.menu_buttons[3][1] == 0:
            pygame.draw.rect(self.screen, (255, 50, 50), (text_x - 10, text_y - 10,
                                                          text_w + 20, text_h + 20), 0)
        elif self.menu_buttons[3][1] == 1:
            pygame.draw.rect(self.screen, (50, 50, 255), (text_x - 10, text_y - 10,
                                                          text_w + 20, text_h + 20), 0)

        self.screen.blit(text, (text_x, text_y))

    def start_plot(self):
        clock = pygame.time.Clock()
        plot_text = open('data/plot.txt', mode='r', encoding='utf-8').read().split('FE')
        for line in plot_text:
            self.screen.fill((100, 100, 100))
            true_text = line.split('\n')
            wait = 0
            for ind, element in enumerate(true_text):
                if 'Продай' not in element and\
                   'овольно' not in element and\
                   'друга' not in element and\
                   'жизнь' not in element:
                    font = pygame.font.Font('data/start_shr.ttf', 50)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 7 - text.get_height() // 2 + 50 * ind
                    text_w = text.get_width()
                    text_h = text.get_height()
                elif 'вольно' in element:
                    font = pygame.font.Font('data/start_shr.ttf', 120)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 8 - text.get_height() // 2 + 50 * ind
                    text_w = text.get_width()
                    text_h = text.get_height()
                elif 'друга' in element or 'жизнь' in element:
                    font = pygame.font.Font('data/start_shr.ttf', 90)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 6 - text.get_height() // 2 + 100 * ind
                    text_w = text.get_width()
                    text_h = text.get_height()
                else:
                    font = pygame.font.Font('data/start_shr.ttf', 200)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 3 - text.get_height() // 2 + 50 * ind
                    text_w = text.get_width()
                    text_h = text.get_height()
                self.screen.blit(text, (text_x, text_y))
                pygame.display.flip()
                clock.tick(2)
                wait = ind
                if element != '\n':
                    clock.tick(2)
            for i in range(wait):
                clock.tick(1)

    def starting_screen(self):  # здесь будет рисоваться стартовый экран
        pass

    def desktop_screen(self):  # здесь будет рисоваться "рабочий" стол
        pass

    def app_end(self):  # действия при завершении работы(для сохранения данных и вывода завершающей анимации)
        self.screen.fill((100, 100, 100))
        pygame.display.flip()
        pygame.quit()


class Background(pygame.sprite.Sprite):  # специальный класс для добавления фонового изображения
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


if __name__ == '__main__':
    app = SellAndGive()
