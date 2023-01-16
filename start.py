# ЗАДАЧИ  !!!

# Начать разработку дата базы для сохранения данных

import pygame
from modules import pygame_button, pygame_image, pygame_text
from win32api import GetSystemMetrics
import os
import sys


class SellAndGive:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.all_screens = ['MainMenu', 'NewGameScreen', 'Desktop', 'Site', 'Continue', 'Authors']

        self.menu_buttons = [['Новая игра', 0], ['Продолжить', 0], ['Авторы', 0],
                             ['Выйти', 0]]  # названия и состояния кнопок

        self.menu_button_location = []  # ЗАПИСЬ ПО СХЕМЕ
        # [x0 - обводка, y0 - обводка, ширина + обводка, высота + обводка] (заполняется в программе)

        self.selected_screen = self.all_screens[0]
        self.start_plot_played = False  # флаг проверки проигрыша сюжета

        self.buttons_start_group = pygame.sprite.Group()
        self.buttons_start_clicked = []  # здесь будет последняя нажатая кнопка при начальном выборе товара
        self.start_text_input = pygame_text.InputBox(self.width - 700, 60, 600, 40, 'ООО"ПродАкшен"')
        start_buttons = [('Начать', (self.width - 300, self.height - 200), '#008000'),
                         ('Попиты', (200, 200), None),
                         ('Скрепки', (200, 400), None),
                         ('Строительный мусор', (200, 600), None)]
        self.start_buttons_info = {'Попиты': 'Самый ходовой товар в вашем городе, \nможно продавать за соответствующую '
                                             'цену\n'
                                             'Делаются в Китае, поэтому \nцена за оптовые закупки высокая,\n'
                                             'Наличие на вашем складе - 10 штук',
                                   'Скрепки': 'Не самый популярный товар в городе, \nдешево продается\n'
                                              'Делаются в местном заводе, поэтому \nцена за оптовые закупки низкая\n'
                                              'Наличие на вашем складе - 20 штук',
                                   'Строительный мусор': 'Популярнее чем скрепки, \nоднако до популярности попитов '
                                                         'далеко\n'
                                                         'Можно найти в окрестностях, \nцена за оптовые закупки '
                                                         'средняя\n'
                                                         'Наличие на вашем складе - 7 штук'}
        for button in start_buttons:
            pygame_button.Button(button[0], button[1], button[2], self.buttons_start_group)

        icons_list = ['browser.png']
        self.desktop_icons_group = pygame.sprite.Group()
        for ind, item in enumerate(icons_list):
            pygame_image.Icon(item, (5, 5 + 100 * ind), self.desktop_icons_group)

        self.app_running()

    def app_running(self):  # старт и работа приложения
        pygame.init()
        mouse_coords = (0, 0)

        pygame.display.set_caption('Продай и отдай')
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        running = True

        cursor = pygame_image.load_image('translucent_pixel.png', -1)
        cursor = pygame.transform.scale(cursor, (40, 50))

        while running:
            for event in pygame.event.get():
                if self.selected_screen == self.all_screens[1]:
                    self.start_text_input.handle_event(event)
                if event.type == pygame.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # выход на кнопку ESC
                    self.app_end()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:  # проверка нажатия мыши

                    if self.selected_screen == self.all_screens[0]:

                        # нажатие по кнопке выхода
                        if self.menu_button_location[3][0] <= event.pos[0] <= \
                                self.menu_button_location[3][0] + self.menu_button_location[3][2] and \
                                self.menu_button_location[3][1] <= event.pos[1] <= \
                                self.menu_button_location[3][1] + self.menu_button_location[3][3]:
                            self.app_end()
                            running = False

                        # нажатие по кнопке Новая Игра
                        elif self.menu_button_location[0][0] <= event.pos[0] <= \
                                self.menu_button_location[0][0] + self.menu_button_location[0][2] and \
                                self.menu_button_location[0][1] <= event.pos[1] <= \
                                self.menu_button_location[0][1] + self.menu_button_location[0][3]:
                            self.selected_screen = self.all_screens[1]

                        # нажатие по кнопке Продолжить
                        elif self.menu_button_location[1][0] <= event.pos[0] <= \
                                self.menu_button_location[1][0] + self.menu_button_location[1][2] and \
                                self.menu_button_location[1][1] <= event.pos[1] <= \
                                self.menu_button_location[1][1] + self.menu_button_location[1][3]:
                            self.selected_screen = self.all_screens[2]

                        # нажатие по кнопке Авторы
                        elif self.menu_button_location[2][0] <= event.pos[0] <= \
                                self.menu_button_location[2][0] + self.menu_button_location[2][2] and \
                                self.menu_button_location[2][1] <= event.pos[1] <= \
                                self.menu_button_location[2][1] + self.menu_button_location[2][3]:
                            self.selected_screen = self.all_screens[3]

                    # кнопки на стартовом экране
                    if self.selected_screen == self.all_screens[1]:
                        for button in self.buttons_start_group.sprites():
                            if button.clicked(event.pos) and button.name != 'Начать':
                                button.tracing = False
                                self.buttons_start_clicked.append(button.name)
                                if len(self.buttons_start_clicked) > 1:
                                    del self.buttons_start_clicked[0]
                            elif button.clicked(event.pos) \
                                    and button.name == 'Начать' \
                                    and bool(self.buttons_start_clicked):
                                self.selected_screen = self.all_screens[2]
                if event.type == pygame.MOUSEMOTION:
                    mouse_coords = event.pos

                    # ограничитель, исключает коллапс с другими экранами
                    if self.selected_screen == self.all_screens[0]:
                        for x, y, w, h in self.menu_button_location:
                            if x <= event.pos[0] <= x + w and y <= event.pos[1] <= y + h:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 1
                            else:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 0

                    if self.selected_screen == self.all_screens[1]:
                        for button in self.buttons_start_group.sprites():
                            if button.clicked(event.pos) \
                                    and button.name not in self.buttons_start_clicked \
                                    and button.name != 'Начать':
                                button.tracing = True
                            elif button.name in self.buttons_start_clicked:
                                button.selected = True
                            else:
                                button.selected = False
                                button.tracing = False

            if not running:
                continue

            if self.selected_screen == 'MainMenu':  # действия при выборе экрана главного меню(по умолчанию)
                self.draw_main_menu()

            elif self.selected_screen == 'NewGameScreen':
                if not self.start_plot_played:
                    self.start_plot()
                    self.start_plot_played = True
                self.starting_screen()

            elif self.selected_screen == 'Desktop':
                self.desktop_screen()

            elif self.selected_screen == 'Site':
                pass

            self.screen.blit(cursor, mouse_coords)
            pygame.display.flip()
            clock.tick(100)

    def draw_main_menu(self):  # перенести сюда простыню из app_running
        menu_background = pygame_image.Image('data/background_menu.png', [0, 0])
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

    def start_plot(self):  # показ сюжета
        clock = pygame.time.Clock()
        skip_plot = False
        plot_text = open('data/plot.txt', mode='r', encoding='utf-8').read().split('FE')
        for line in plot_text:  # для каждой страницы ('FE')
            self.screen.fill((100, 100, 100))
            true_text = line.split('\n')
            wait = 0
            if skip_plot:
                break
            for ind, element in enumerate(true_text):  # для каждой строчки
                if skip_plot:
                    break
                if 'Продай' not in element and \
                        'овольно' not in element and \
                        'друга' not in element and \
                        'жизнь' not in element:
                    font = pygame.font.Font('text_fonts/start_shr.ttf', 50)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 7 - text.get_height() // 2 + 50 * ind

                elif 'вольно' in element:
                    font = pygame.font.Font('text_fonts/start_shr.ttf', 120)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 8 - text.get_height() // 2 + 50 * ind

                elif 'друга' in element or 'жизнь' in element:
                    font = pygame.font.Font('text_fonts/start_shr.ttf', 90)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 6 - text.get_height() // 2 + 100 * ind

                else:
                    font = pygame.font.Font('text_fonts/start_shr.ttf', 200)
                    text = font.render(element, True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 1.92 - text.get_width() // 2 - 50
                    text_y = self.height // 3 - text.get_height() // 2 + 50 * ind

                self.screen.blit(text, (text_x, text_y))
                pygame.display.flip()
                clock.tick(2)
                wait = ind
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        skip_plot = True
                if element != '\n':
                    clock.tick(2)
            for i in range(wait):
                if not skip_plot:
                    clock.tick(3)
                else:
                    clock.tick(999999)

    def starting_screen(self):  # здесь будет рисоваться стартовый экран
        screen_background = pygame_image.Image('data/computer_prototype.png')
        name_label = pygame_text.label('Введите название магазина:', (self.width - 1250, 50))
        tip = '\nПОДСКАЗКА: Помните, что завершая день\n'\
              'На счету должно оставаться как минимум 10 рублей!\n'\
              'Иначе вы умрете от голода.'
        self.screen.blit(screen_background.image, screen_background.rect)
        for button in self.buttons_start_group.sprites():
            if button.tracing:
                pygame.draw.rect(self.screen, pygame.Color(150, 150, 150), (
                    button.rect[0] - 50, button.rect[1], button.rect[0] + button.size[0], button.size[1]))
            elif button.selected and button.name != 'Начать':
                info = self.start_buttons_info[button.name].split('\n')
                for ind, element in enumerate(info):
                    info_label = pygame_text.label(element, (self.width - 850, 150 + 75 * ind), None)
                    self.screen.blit(info_label[0], info_label[1])
                pygame.draw.rect(self.screen, pygame.Color(50, 50, 50), (
                    button.rect[0] - 50, button.rect[1], button.rect[0] + button.size[0], button.size[1]))

        self.start_text_input.update()
        self.screen.blit(name_label[0], name_label[1])
        for ind, text in enumerate(tip.split('\n')):
            tip_label = pygame_text.label(text, (200, 700 + 50 * ind))
            self.screen.blit(tip_label[0], tip_label[1])
        self.start_text_input.draw(self.screen)
        self.buttons_start_group.draw(self.screen)

    def desktop_screen(self):  # здесь будет рисоваться "рабочий" стол
        desktop_background = pygame_image.Image('data/desktop.png', resize=True)
        self.screen.blit(desktop_background.image, desktop_background.rect)
        self.desktop_icons_group.draw(self.screen)

    def app_end(self):  # действия при завершении работы(для сохранения данных и вывода завершающей анимации)
        self.screen.fill((100, 100, 100))
        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    app = SellAndGive()
