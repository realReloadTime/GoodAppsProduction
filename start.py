import pygame
from modules import pygame_button, pygame_image, pygame_text
from win32api import GetSystemMetrics
import sqlite3
import shutil
import os
from random import randint, choice
# f

class SellAndGive:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.all_screens = ['MainMenu', 'NewGameScreen', 'Desktop', 'Site', 'Warehouse',
                            'Logistics', 'Purchase', 'Continue', 'Authors', 'Growth']

        self.menu_buttons = [['Новая игра', 0], ['Продолжить', 0], ['Авторы', 0],
                             ['Выйти', 0]]  # названия и состояния кнопок

        self.menu_button_location = []  # ЗАПИСЬ ПО СХЕМЕ
        # [x0 - обводка, y0 - обводка, ширина + обводка, высота + обводка] (заполняется в программе)

        self.selected_screen = self.all_screens[0]
        self.start_plot_played = False  # флаг проверки проигрыша сюжета
        self.text = ''
        self.warehouse_status = ''
        self.purchase_status = ''
        self.transport_index = 0

        self.tasks = [False for _ in range(5)]

        self.buttons_start_group = pygame.sprite.Group()
        self.buttons_start_clicked = []  # здесь будет последняя нажатая кнопка при начальном выборе товара
        self.start_text_input = pygame_text.InputBox(self.width - 700, 60, 600, 40, 'ООО"ПродАкшен"')
        start_buttons = [('Начать', (self.width - 300, self.height - 200), '#008000'),
                         ('Попиты', (200, 200), '#e55c5c'),
                         ('Скрепки', (200, 400), '#e55c5c'),
                         ('Строительный мусор', (200, 600), '#e55c5c')]
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
        self.task_list = [[], [], [], [], [], []]
        self.task_names = ['Дядя Вася', 'Отец Евгений', 'Зиновор', 'Брат Зохраб', 'Золибек', 'Вордазар', 'Востинак',
                           'Папин', 'Казимир', 'Тётя Забэл', 'Зинаида', 'Брат Радован', 'Ратибор', 'Роман', 'Сестра Ия',
                           'Дядя Иты', 'Прабабушка Инга', 'Cестра Генриетта', 'Градислава',
                           'Груня', 'Брат Чеслав', 'Папа дяди Эраста', 'Даниил', 'Дмитрий', 'Доброслав',
                           'Добросмысл', 'Дед Дорофей', 'Бабушка Оксана', 'Анастасия', 'Алиса', 'Тётя Жанна', 'Тамара',
                           'Дед Агафон', 'Юрий', 'Незнакомец', 'Незнакомка', 'ТоТ_СаМыЙ', 'Снегр', 'Мечта',
                           'Оксана 100м.', 'Аверкий', 'Тётя Ева', 'Диана', 'Вивея', 'Артём', 'Тихон', 'Самсон',
                           'Полерия', 'Ангелина', 'Регина', 'Ульяна', 'Олег']
        self.customers_count = 0
        for button in start_buttons:
            pygame_button.Button(button[0], button[1], button[2], self.buttons_start_group)

        icons_list = ['browser.png', 'warehouse.png', 'logistic.png', 'purchase.png', 'growth_point.png', 'vacation.png']
        self.desktop_icons_group = pygame.sprite.Group()
        pygame_image.Icon('clear_image.png', (self.width - 350, 5), self.desktop_icons_group)
        for sprite in self.desktop_icons_group.sprites():
            if sprite.name == 'clear_image.png':
                sprite.add_text('Следующий день', size=50, color='red')
        for ind, item in enumerate(icons_list):
            if item != 'vacation.png':
                pygame_image.Icon(item, (5, 5 + 210 * ind), self.desktop_icons_group)
            else:
                pygame_image.Icon(item, (self.width - 300, 100), self.desktop_icons_group)
        self.desktop_status = ''

        self.warehouse_icons_groups = pygame.sprite.Group()
        icons = [('back_to_desktop.png', (self.width - 225, 5))]
        for icon in icons:
            pygame_image.Icon(icon[0], icon[1], self.warehouse_icons_groups)

        self.site_buttons_group = pygame.sprite.Group()
        self.purchase_buttons_group = pygame.sprite.Group()
        buttons = [('back_to_desktop.png', (self.width - 225, 5))]
        for icon in buttons:
            pygame_image.Icon(icon[0], icon[1], self.purchase_buttons_group)
        self.goods = []
        self.logistics_buttons_group = pygame.sprite.Group()
        buttons = [('back_to_desktop.png', (self.width - 225, 5)), ('left_arrow.png', (self.width - 1325, self.height // 2 - 100)),
                   ('right_arrow.png', (self.width - 825, self.height // 2 - 100))]
        for icon in buttons:
            pygame_image.Icon(icon[0], icon[1], self.logistics_buttons_group)
        pygame_button.Button(f'Купить за 1100 рублей', (self.width // 2 - 400, self.height - 400), 'black', self.logistics_buttons_group)
        self.logistics_status = ''
        self.growth_buttons_group = pygame.sprite.Group()
        buttons = [('back_to_desktop.png', (self.width - 225, 5)),
                   ('left_arrow.png', (250, self.height // 2 - 100)),
                   ('right_arrow.png', (self.width - 500, self.height // 2 - 100))]
        pygame_button.Button(f'Купить за 1000 рублей', (self.width // 2 - 450, self.height - 150), 'black',
                             self.growth_buttons_group)
        for icon in buttons:
            pygame_image.Icon(icon[0], icon[1], self.growth_buttons_group)
        self.growth_count = 0
        self.growth_status = ''

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

                if event.type == pygame.MOUSEBUTTONUP:  # проверка нажатия мыши

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
                            self.selected_screen = self.all_screens[self.all_screens.index('Continue')]

                        # нажатие по кнопке Авторы
                        elif self.menu_button_location[2][0] <= event.pos[0] <= \
                                self.menu_button_location[2][0] + self.menu_button_location[2][2] and \
                                self.menu_button_location[2][1] <= event.pos[1] <= \
                                self.menu_button_location[2][1] + self.menu_button_location[2][3]:
                            self.selected_screen = self.all_screens[-1]

                    # кнопки на стартовом экране
                    elif self.selected_screen == self.all_screens[1]:
                        for button in self.buttons_start_group.sprites():
                            if button.clicked(event.pos) and button.name != 'Начать':
                                button.tracing = False
                                self.buttons_start_clicked.append(button.name)
                                if len(self.buttons_start_clicked) > 1:
                                    del self.buttons_start_clicked[0]
                            elif button.clicked(event.pos) \
                                    and button.name == 'Начать' \
                                    and bool(self.buttons_start_clicked):
                                if os.path.exists('data/saved_data.db'):
                                    os.remove('data/saved_data.db')
                                    shutil.copy('data/data_sample.db', 'data/saved_data.db')
                                else:
                                    shutil.copy('data/data_sample.db', 'data/saved_data.db')

                                self.con = sqlite3.connect("data/saved_data.db")
                                self.cur = self.con.cursor()

                                self.cur.execute("""INSERT INTO shop_data(name, money, transport, 
                                customers_multiplier, failure_multiplier, price_multiplier, level, day) 
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                                                 (self.start_text_input.text, 1030, 1, 0.5, 0.5, 0.5, 1, 0)).fetchall()
                                self.con.commit()
                                if self.buttons_start_clicked[0] == 'Попиты':
                                    count = 10
                                elif self.buttons_start_clicked[0] == 'Скрепки':
                                    count = 20
                                elif self.buttons_start_clicked[0] == 'Строительный мусор':
                                    count = 7
                                self.cur.execute("""INSERT INTO warehouse(name, count) VALUES(?, ?)""",
                                                 (self.buttons_start_clicked[0], count))
                                self.con.commit()
                                self.next_day()
                                self.selected_screen = self.all_screens[2]

                    elif self.selected_screen == self.all_screens[2]:
                        for icon in self.desktop_icons_group.sprites():
                            if icon.clicked(event.pos):
                                if icon.name == 'browser.png':
                                    self.selected_screen = self.all_screens[3]
                                elif icon.name == 'warehouse.png':
                                    self.selected_screen = self.all_screens[4]
                                elif icon.name == 'logistic.png':
                                    self.selected_screen = self.all_screens[5]
                                elif icon.name == 'purchase.png':
                                    self.selected_screen = self.all_screens[6]
                                elif icon.name == 'clear_image.png':
                                    self.next_day()
                                elif icon.name == 'growth_point.png':
                                    self.selected_screen = self.all_screens[-1]
                                elif icon.name == 'vacation.png':
                                    money = self.cur.execute("""SELECT money FROM shop_data""").fetchone()[0]
                                    if money >= 100000:
                                        self.vacation_screen()
                                    else:
                                        self.desktop_status = 'Чтобы отправиться в отпуск нужно накопить 100 тысяч рублей'

                    elif self.selected_screen == self.all_screens[3]:
                        for button in self.site_buttons_group.sprites():
                            if 'back_to' in button.name and button.clicked(event.pos):
                                self.selected_screen = self.all_screens[2]
                            elif button.clicked(event.pos):
                                self.text = 'Статус заказов: '
                                customers = self.cur.execute("""SELECT good_name, count FROM customers""").fetchall()
                                number = int(button.name.split('№')[-1])
                                warehouse = self.cur.execute("""SELECT * FROM warehouse""").fetchall()
                                warehouse_names = [x[0] for x in warehouse]
                                item = customers[number - 1][0]

                                if item in warehouse_names and not self.tasks[number - 1]:
                                    if customers[number - 1][1] <= warehouse[warehouse_names.index(item)][1]:
                                        self.cur.execute("""UPDATE warehouse
                                        SET count=(?)
                                        WHERE name=(?)""", (warehouse[warehouse_names.index(item)][1] - customers[number - 1][1], item))
                                        self.con.commit()
                                        self.text += f'заказ #{number} доставляется'
                                        income = self.cur.execute("""SELECT sale_price FROM goods_types WHERE name=?""", (item, )).fetchone()[0] * customers[number - 1][1]
                                        self.cur.execute("""INSERT INTO delivery_process(name, income, arrive) VALUES (?, ?, (SELECT delivery_time FROM transport_types WHERE id=(SELECT transport FROM shop_data)))""", (item, income))
                                        self.con.commit()
                                        self.tasks[number - 1] = True

                                    else:
                                        self.text += 'недостаточное количество товара на складе'
                                        self.tasks[number - 1] = False
                                else:
                                    self.text += 'товар отсутствует на складе'
                                    self.tasks[number - 1] = False

                    elif self.selected_screen == self.all_screens[4]:
                        for icon in self.warehouse_icons_groups.sprites():
                            if icon.clicked(event.pos):
                                if icon.name == 'back_to_desktop.png':
                                    self.selected_screen = self.all_screens[2]

                    elif self.selected_screen == self.all_screens[5]:
                        for icon in self.logistics_buttons_group.sprites():
                            if icon.clicked(event.pos):
                                if icon.name == 'back_to_desktop.png':
                                    self.selected_screen = self.all_screens[2]
                                    self.logistics_status = ''
                                elif icon.name == 'left_arrow.png':
                                    self.transport_index -= 1
                                elif icon.name == 'right_arrow.png':
                                    self.transport_index += 1
                                elif 'Купить' in icon.name and icon.clicked(event.pos):
                                    money = self.cur.execute("""SELECT money FROM shop_data""").fetchone()[0]
                                    transport = self.cur.execute("""SELECT name FROM transport_types WHERE price = ?""", (int(icon.name.split()[-2]), )).fetchone()[0]
                                    if money >= int(icon.name.split()[-2]):
                                        self.cur.execute("""UPDATE shop_data SET transport = (SELECT id FROM transport_types WHERE name = ?)""", (transport, ))
                                        self.con.commit()
                                        self.logistics_status = 'Успешная покупка'

                                    else:
                                        self.logistics_status = 'Недостаточно средств для покупки'

                            if 'Купить' in icon.name:
                                self.logistics_buttons_group.remove(icon)
                                my_transport = self.cur.execute("""SELECT transport FROM shop_data""").fetchone()[0]
                                transport_kinds = self.cur.execute("""SELECT price FROM transport_types WHERE id != ?""",
                                                                   (my_transport,)).fetchall()

                                self.transport_index = self.transport_index % len(transport_kinds)
                                pygame_button.Button(f'Купить за {str(transport_kinds[self.transport_index][0])} рублей', (self.width // 2 - 420, self.height - 400), 'black', self.logistics_buttons_group)

                    elif self.selected_screen == self.all_screens[6]:
                        for icon in self.purchase_buttons_group.sprites():
                            if icon.clicked(event.pos):
                                if icon.name == 'back_to_desktop.png':
                                    self.selected_screen = self.all_screens[2]
                                    self.purchase_status = ''
                                else:
                                    self.buying_process(icon.name)

                    elif self.selected_screen == self.all_screens[-1]:
                        for icon in self.growth_buttons_group.sprites():
                            if icon.clicked(event.pos):
                                if icon.name == 'back_to_desktop.png':
                                    self.selected_screen = self.all_screens[2]
                                    self.growth_status = ''
                                elif icon.name == 'left_arrow.png':
                                    self.growth_count -= 1
                                elif icon.name == 'right_arrow.png':
                                    self.growth_count += 1
                                elif 'Купить' in icon.name and icon.clicked(event.pos):
                                    money = self.cur.execute("""SELECT money FROM shop_data""").fetchone()[0]
                                    growth_kinds = self.cur.execute(
                                        """SELECT cost, name FROM business_levels WHERE id != (SELECT level FROM shop_data)""").fetchall()
                                    cost = int(growth_kinds[self.growth_count][0])

                                    if money >= cost:
                                        self.cur.execute("""UPDATE shop_data SET money = ?, level = (SELECT id FROM business_levels WHERE name = ?)""", (money - cost, growth_kinds[self.growth_count][1]))
                                        self.con.commit()
                                        self.growth_status = 'Успешная покупка'

                                    else:
                                        self.growth_status = 'Недостаточно средств для покупки'

                            if 'Купить' in icon.name:
                                self.growth_buttons_group.remove(icon)
                                growth_kinds = self.cur.execute("""SELECT cost FROM business_levels WHERE id != (SELECT level FROM shop_data)""").fetchall()
                                self.growth_count = self.growth_count % len(growth_kinds)
                                cost = int(growth_kinds[self.growth_count][0])

                                pygame_button.Button(
                                    f'Купить за {str(cost)} рублей',
                                    (self.width // 2 - 450, self.height - 150), 'black', self.growth_buttons_group)



                if event.type == pygame.MOUSEMOTION:
                    mouse_coords = event.pos

                    # ограничитель, исключает коллапс с другими экранами
                    if self.selected_screen == self.all_screens[0]:
                        for x, y, w, h in self.menu_button_location:
                            if x <= event.pos[0] <= x + w and y <= event.pos[1] <= y + h:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 1
                            else:
                                self.menu_buttons[self.menu_button_location.index([x, y, w, h])][1] = 0

                    elif self.selected_screen == self.all_screens[1]:
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
                    elif self.selected_screen == self.all_screens[2]:
                        for icon in self.desktop_icons_group.sprites():
                            if icon.clicked(event.pos):
                                icon.tracing = True
                            else:
                                icon.tracing = False
                    elif self.selected_screen == self.all_screens[3]:
                        for button in self.site_buttons_group.sprites():
                            if button.clicked(event.pos):
                                button.tracing = True
                            else:
                                button.tracing = False

                    elif self.selected_screen == self.all_screens[4]:
                        for icon in self.warehouse_icons_groups.sprites():
                            if icon.clicked(event.pos):
                                icon.tracing = True
                            else:
                                icon.tracing = False

                    elif self.selected_screen == self.all_screens[6]:
                        for icon in self.purchase_buttons_group.sprites():
                            if icon.clicked(event.pos):
                                icon.tracing = True
                            else:
                                icon.tracing = False

                    elif self.selected_screen == self.all_screens[-1]:
                        for icon in self.growth_buttons_group.sprites():
                            if icon.clicked(event.pos):
                                icon.tracing = True
                            else:
                                icon.tracing = False

            if not running:
                continue

            if self.selected_screen == 'MainMenu':  # действия при выборе экрана главного меню(по умолчанию)
                self.draw_main_menu()

            elif self.selected_screen == 'NewGameScreen':
                if not self.start_plot_played:
                    self.start_plot()
                    self.start_plot_played = True
                self.starting_screen()

            elif self.selected_screen == 'Continue':
                if os.path.exists('data/saved_data.db'):
                    self.add_cur_and_con()
                    self.selected_screen = self.all_screens[self.all_screens.index('Desktop')]
                    self.goods = self.cur.execute(
                        """SELECT * FROM goods_types WHERE opening_level BETWEEN 1 and (SELECT level FROM shop_data)""").fetchall()
                else:
                    self.selected_screen = self.all_screens[1]


            elif self.selected_screen == 'Desktop':
                self.desktop_screen()

            elif self.selected_screen == 'Site':
                self.site_screen()

            elif self.selected_screen == 'Warehouse':
                self.warehouse_screen()

            elif self.selected_screen == 'Logistics':
                self.logistics_screen()

            elif self.selected_screen == 'Purchase':
                self.purchase_screen()

            elif self.selected_screen == 'Growth':
                self.growth_point()

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
        tip = '\nПОДСКАЗКА: Помните, что завершая день\n' \
              'На счету должно оставаться как минимум 10 рублей!\n' \
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
        money = self.cur.execute('''SELECT money FROM shop_data''').fetchone()[0]
        money_count = pygame_text.label(f'Кошелек: {money} рублей', (self.width, self.height))
        self.screen.blit(desktop_background.image, desktop_background.rect)
        self.screen.blit(money_count[0], (money_count[1][0] - money_count[2], money_count[1][1] - money_count[3]))
        for icon in self.desktop_icons_group:
            if icon.tracing and icon.name != 'clear_image.png':
                pygame.draw.rect(self.screen, pygame.Color(200, 200, 200), (
                    icon.rect[0] + 25, icon.rect[1] + 5, icon.rect[0] + icon.size[0] - 50, icon.size[1]))
                pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), (
                    icon.rect[0] + 25, icon.rect[1] + 5, icon.rect[0] + icon.size[0] - 50, icon.size[1]), 3)
            elif icon.tracing and icon.name == 'clear_image.png':
                icon.add_text('Следующий день', size=50, color='green')
            elif not icon.tracing and icon.name == 'clear_image.png':
                icon.add_text('Следующий день', size=50, color='red')
        self.text = ''
        label = pygame_text.label(self.desktop_status, (self.width - 500, self.height - 10))
        self.screen.blit(label[0], label[1])

        self.desktop_icons_group.draw(self.screen)

    def site_screen(self):
        site_background = pygame_image.Image('data/background_site.png', [0, 0])
        addres_pic = pygame_image.Image('adress.png', [0, 5], clear_background=True)
        self.screen.blit(site_background.image, site_background.rect)
        self.screen.blit(addres_pic.image, addres_pic.rect)

        for button in self.site_buttons_group.sprites():
            if button.tracing:
                pygame.draw.rect(self.screen, pygame.Color(150, 150, 20), (
                    button.coords[0], button.coords[1], button.size[0], button.size[1]), 3)
            if '1' in button.name and self.tasks[0]:
                button.cross()
            elif '2' in button.name and self.tasks[1]:
                button.cross()
            elif '3' in button.name and self.tasks[2]:
                button.cross()
            elif '4' in button.name and self.tasks[3]:
                button.cross()
            elif '5' in button.name and self.tasks[4]:
                button.cross()
        customers = self.cur.execute("""SELECT * FROM customers""").fetchall()
        if len(customers) != self.customers_count:
            self.customers_count = len(customers)
            for sprite in self.site_buttons_group.sprites():
                self.site_buttons_group.remove(sprite)
        transport = self.cur.execute("""SELECT * FROM transport_types WHERE id = (SELECT transport FROM shop_data)""").fetchone()
        business = self.cur.execute("""SELECT name FROM business_levels WHERE id = (SELECT level FROM shop_data)""").fetchone()
        info = pygame_text.label('Информация', (40, 790), color='#eb5a26')
        transport_info = pygame_text.label(f'Текущий транспорт: {transport[1]}, время доставки: {transport[3]} сут.', (40, 850), color='#eb5a26')
        business_level = pygame_text.label(f'Уровень бизнеса: {business[0]}', (40, 910), color='#eb5a26')

        width, height = transport_info[2], transport_info[3]

        pygame.draw.rect(self.screen, pygame.Color('blue'), (info[1][0] - 5, info[1][1], width + 5, height + 125), 2)

        self.screen.blit(info[0], info[1])
        self.screen.blit(transport_info[0], transport_info[1])
        self.screen.blit(business_level[0], business_level[1])

        shop_name, money = self.cur.execute('''SELECT name, money FROM shop_data''').fetchone()
        shop_name = pygame_text.label('Интернет-магазин ' + shop_name, (self.width, 150))
        money_count = pygame_text.label(f'Кошелек: {money} рублей', (self.width, self.height))

        for index, customer in enumerate(customers):
            cust_label = pygame_text.label(f'{index + 1}. Заказ от {customer[1]}: {customer[2]}, {customer[3]} шт.', (50, 300 + 100 * index))
            self.screen.blit(cust_label[0], cust_label[1])

        site_buttons = [('back_to_desktop(site).png', (self.width - 175, 5))] + [(f'Принять заказ №{x + 1}', (self.width - 800, 260 + 100 * x)) for x in range(len(customers))]
        sprite_names = [x.name for x in self.site_buttons_group.sprites()]
        for button in site_buttons:
            if button[0] not in sprite_names:
                pygame_button.Button(button[0], button[1], 'black', self.site_buttons_group)

        status_label = pygame_text.label(self.text, (5, self.height - 30), None, 30)

        self.screen.blit(status_label[0], status_label[1])
        self.site_buttons_group.draw(self.screen)
        self.screen.blit(shop_name[0], ((shop_name[1][0] - shop_name[2]) // 2, shop_name[1][1]))
        self.screen.blit(money_count[0], (money_count[1][0] - money_count[2], money_count[1][1] - money_count[3]))

    def warehouse_screen(self):
        warehouse_background = pygame_image.Image('data/background_storage.png', [0, 0], resize=True)
        self.screen.blit(warehouse_background.image, warehouse_background.rect)
        for button in self.warehouse_icons_groups.sprites():
            if button.tracing:
                pygame.draw.rect(self.screen, pygame.Color(0, 100, 50), (
                    button.coords[0], button.coords[1], button.size[0], button.size[1]), 3)  # координаты верхнего левого
                # угла, ширина, высота
        items = self.cur.execute('''SELECT * FROM warehouse''').fetchall()
        label_total = pygame_text.label('В НАЛИЧИИ', (90, 120), size=70)

        self.screen.blit(label_total[0], label_total[1])
        for ind, item in enumerate(items):
            item = map(str, item)
            label = pygame_text.label(': '.join(item), (25, 240 + ind * 75))
            self.screen.blit(label[0], label[1])

        for index, element in enumerate(self.warehouse_status.split('\n')):
            status_label = pygame_text.label(element, (self.width - 700, 200 + 50 * index), None)
            self.screen.blit(status_label[0], status_label[1])
        self.warehouse_icons_groups.draw(self.screen)

    def logistics_screen(self):
        logistics_background = pygame_image.Image('data/background_logistic.png', [0, 0], resize=True)
        self.screen.blit(logistics_background.image, logistics_background.rect)
        my_transport = self.cur.execute("""SELECT transport FROM shop_data""").fetchone()[0]
        transport_kinds = self.cur.execute("""SELECT * FROM transport_types WHERE id != ?""", (my_transport, )).fetchall()
        transport = pygame_text.label(transport_kinds[self.transport_index][1],
                                      (self.width // 2 - 180, self.height // 2 - 65), size=100)
        delivery_time = pygame_text.label(f'Время доставки: {transport_kinds[self.transport_index][3]}', (self.width // 2 - 400, self.height - 290))
        delivery_price = pygame_text.label(f'Цена доставки: {transport_kinds[self.transport_index][4]}', (self.width // 2 - 400, self.height - 240))
        self.screen.blit(delivery_time[0], delivery_time[1])
        self.screen.blit(delivery_price[0], delivery_price[1])
        self.logistics_buttons_group.draw(self.screen)
        self.screen.blit(transport[0], transport[1])
        label = pygame_text.label(self.logistics_status, (10, self.height - 100))
        self.screen.blit(label[0], label[1])

    def purchase_screen(self):
        purchase_background = pygame_image.Image('data/background_purchase.png', [0, 0], resize=True)
        self.screen.blit(purchase_background.image, purchase_background.rect)
        for button in self.purchase_buttons_group.sprites():
            if button.tracing:
                pygame.draw.rect(self.screen, pygame.Color(250, 0, 0), (
                    button.coords[0], button.coords[1], button.size[0], button.size[1]), 3)
        for index, item in enumerate(self.goods):
            pygame_button.Button(f'<{item[1]}> - {item[3]} шт. Цена: {item[2]}', (20, 100 + 100 * index), '#0911ab', self.purchase_buttons_group)
        self.purchase_buttons_group.draw(self.screen)
        purchase_status = pygame_text.label(self.purchase_status, (5, self.height - 50))
        self.screen.blit(purchase_status[0], purchase_status[1])

    def buying_process(self, name):
        money, level = self.cur.execute("""SELECT money, level FROM shop_data""").fetchone()
        money, level = int(money), int(level)
        name = name.split('>')[0][1:]
        capacity = self.cur.execute("""SELECT capacity FROM business_levels WHERE id = ?""", (level, )).fetchone()[0]
        price, count = self.cur.execute("""SELECT purchase_price, purchase_count FROM goods_types WHERE name = ?""", (name, )).fetchone()
        warehouse = self.cur.execute("""SELECT * FROM warehouse""").fetchall()
        capacity_count = sum([x[1] for x in warehouse])
        not_in_warehouse = not any(name == x[0] for x in warehouse)
        if money >= price and capacity - capacity_count >= count:
            if not_in_warehouse:
                self.cur.execute("""INSERT INTO warehouse(name, count) VALUES(?, ?)""", (name, count))
                self.con.commit()
            else:
                self.cur.execute("""UPDATE warehouse SET count = count + ? WHERE name = ?""", (count, name))
                self.con.commit()
            self.purchase_status = 'Успешно куплено'
            self.cur.execute("""UPDATE shop_data SET money = money - ?""", (price, ))
        else:
            self.purchase_status = f'Ошибка, не хватает денег или места на складе. Текущая вместимость: {capacity}'

    def goods_today(self):
        self.goods = self.cur.execute(
            """SELECT * FROM goods_types WHERE opening_level BETWEEN 1 and (SELECT level FROM shop_data)""").fetchall()
        while len(self.goods) > 5:
            del self.goods[randint(0, len(self.goods) - 1)]

    def promotion_screen(self):
        pass

    def growth_point(self):
        growth_kinds = self.cur.execute("""SELECT * FROM business_levels WHERE id != (SELECT level FROM shop_data)""").fetchall()
        growth_point_background = pygame_image.Image('data/hangar.png', [0, 0], resize=True)
        self.screen.blit(growth_point_background.image, growth_point_background.rect)
        self.growth_count = self.growth_count % len(growth_kinds)
        level = pygame_text.label(growth_kinds[self.growth_count][1],
                                      (self.width // 2 - 550, self.height // 2 - 65), size=100)
        capacity = pygame_text.label(f'Вместимость: {growth_kinds[self.growth_count][2]}',
                                           (self.width // 2 - 600, self.height - 350))
        for button in self.growth_buttons_group.sprites():
            if button.tracing and button.name != 'right_arrow.png' and button.name != 'left_arrow.png':
                pygame.draw.rect(self.screen, pygame.Color(255, 255, 255), (
                    button.coords[0] - 5, button.coords[1], button.size[0], button.size[1]))
                pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), (
                    button.coords[0] - 5, button.coords[1], button.size[0], button.size[1]), 2)

        label = pygame_text.label(self.growth_status, (10, self.height - 204))
        self.screen.blit(label[0], label[1])

        self.growth_buttons_group.draw(self.screen)
        self.screen.blit(level[0], level[1])
        self.screen.blit(capacity[0], capacity[1])

    def vacation_screen(self):
        coords = [0, self.height]
        clock = pygame.time.Clock()
        while coords[1] > -20:
            game_over = pygame_image.Image('data/over.png', coords)
            self.screen.blit(game_over.image, game_over.rect)
            pygame.display.flip()
            coords[1] -= 20
            clock.tick(20)
        for i in range(10):
            clock.tick(1)
        self.selected_screen = self.all_screens[2]
        self.cur.execute("""UPDATE shop_data SET money = money - 100000""")
        self.con.commit()

    def add_cur_and_con(self):
        self.con = sqlite3.connect("data/saved_data.db")
        self.cur = self.con.cursor()

    def next_day(self):
        for sprite in self.site_buttons_group.sprites():
            self.site_buttons_group.remove(sprite)
        self.goods_today()
        self.warehouse_status = ''
        self.tasks = [False for _ in range(5)]
        money, transport = self.cur.execute("""SELECT money, transport FROM shop_data""").fetchall()[0]
        if money >= 0:
            self.cur.execute("""UPDATE delivery_process
            SET arrive = arrive - 1""")
            self.con.commit()
            arrives = self.cur.execute("""SELECT * FROM delivery_process""").fetchall()
            self.cur.execute("""DELETE from delivery_process WHERE arrive = 0""")
            self.con.commit()
            plus = 0
            for element in arrives:
                if element[3] == 0:
                    plus += element[2]
                    self.warehouse_status += f'Товар {element[1]} доставлен.\nПрибыль: {element[2]}\n\n'
            self.cur.execute("""UPDATE shop_data 
            SET money = money + ?""", (plus, ))
            self.con.commit()
            self.task_list = [[] for i in range(6)]
            res = self.cur.execute("""SELECT * FROM goods_types 
            WHERE opening_level BETWEEN 1 AND (SELECT level FROM shop_data)""").fetchall()
            while len(res) > 5:
                del res[randint(1, len(res) - 1)]
            level = int(self.cur.execute("""SELECT level FROM shop_data""").fetchall()[0][0])

            self.cur.execute("""UPDATE shop_data
            SET money = money - ?""", (level * 30, ))
            self.con.commit()
            delivery_time = self.cur.execute("""SELECT delivery_time 
            FROM transport_types WHERE id=?""", (transport, )).fetchone()[0]
            delivery_cost = [x[0] for x in self.cur.execute("""SELECT delivery_cost FROM transport_types""").fetchall()]
            warehouse_names = [''.join(x) for x in self.cur.execute("""SELECT name FROM warehouse""").fetchall()]
            warehouse_count = [x[0] for x in self.cur.execute("""SELECT count FROM warehouse""").fetchall()]

            for element in res:
                if element in warehouse_names:
                    count = randint(1, warehouse_count[warehouse_names.index(element)] + 3)
                    while ((count - warehouse_count[warehouse_names.index(element)]) * int(element[2]) +
                           delivery_cost[transport - 1] + level * 30 * delivery_time) >= money:
                        count = randint(1, warehouse_count[warehouse_names.index(element)] + 3)
                        if warehouse_count[warehouse_names.index(element)] * int(element[2]) + delivery_cost[transport - 1] >= money:
                            count = randint(1, warehouse_count[warehouse_names.index(element)] + 3)
                            break
                else:
                    count = randint(1, element[3] + 1)
                    while (count * int(element[2]) + delivery_cost[transport - 1] + level * 30 * delivery_time) >= money:
                        count = randint(1, element[3] + 1)
                        if count * int(element[2]) + delivery_cost[transport - 1] >= money:
                            count = randint(1, element[3] + 1)
                            break
                name = choice(self.task_names)

                self.task_list[int(element[5])].append((name, element[1], count))

            self.cur.execute("""DELETE from customers""")
            self.con.commit()

            for level in self.task_list:
                for task in level:
                    self.cur.execute("""INSERT INTO customers(name, good_name, count) VALUES(?, ?, ?)""",
                                     (task[0], task[1], task[2]))
                    self.con.commit()
        else:
            self.game_over()

    def game_over(self):
        coords = [self.width, 0]
        clock = pygame.time.Clock()
        while coords[0] > -20:
            game_over = pygame_image.Image('data/game_over.png', coords)
            self.screen.blit(game_over.image, game_over.rect)
            pygame.display.flip()
            coords[0] -= 20
            clock.tick(20)
        for i in range(10):
            clock.tick(1)
        self.con.close()
        os.remove('data/saved_data.db')
        self.selected_screen = self.all_screens[0]

    def app_end(self):  # действия при завершении работы(для сохранения данных и вывода завершающей анимации)
        self.screen.fill((100, 100, 100))
        pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    app = SellAndGive()
