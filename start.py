# ЗАДАЧИ  !!!
# Нарисовать фоны для экранов, анимации(не в приоритете)
# Перенести код отрисовки главного меню в специальную функцию draw_menu
# Начать разработку дата базы для сохранения данных
import pygame
from win32api import GetSystemMetrics


class SellAndGive:
    def __init__(self):
        # взять размеры экрана (нужно для правильного расположения объектов на любом экране)
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        self.screen = pygame.display.set_mode((self.width, self.height))

        # менеджер экранов для удобного переключения между ними(список будет расширяться)
        self.all_screens = ['MainMenu', 'NewGameScreen', 'Desktop', 'Site']

        # отмечаем выбранный экран
        self.selected_screen = self.all_screens[0]

        # запускаем приложение
        self.app_running()

    def app_running(self):  # старт и работа приложения
        pygame.init()

        pygame.display.set_caption('Продай и отдай')
        clock = pygame.time.Clock()
        buttons = [['Новая игра', 0], ['Продолжить', 0], ['Авторы', 0], ['Выйти', 0]]  # названия и состояния кнопок

        # расположение кнопок
        button_location = []  # ЗАПИСЬ ПО СХЕМЕ [x0 - обводка, y0 - обводка, ширина + обводка, высота + обводка]
        running = True

        while running:
            self.screen.fill((31, 204, 255))  # голубой цвет(заглушка для фона)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # выход на кнопку ESC
                    self.app_end()
                    running = False

                if event.type == pygame.MOUSEMOTION:

                    # ограничитель, исключает коллапс с другими экранами
                    if self.selected_screen == self.all_screens[0]:
                        for x, y, w, h in button_location:
                            if x <= event.pos[0] <= x + w and y <= event.pos[1] <= y + h:
                                buttons[button_location.index([x, y, w, h])][1] = 1
                            else:
                                buttons[button_location.index([x, y, w, h])][1] = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_location[3][0] <= event.pos[0] <= button_location[3][0] + button_location[3][2] and\
                            button_location[3][1] <= event.pos[1] <= button_location[3][1] + button_location[3][3]:
                        running = False
            if not running:
                continue

            if self.selected_screen == 'MainMenu':  # действия при выборе экрана главного меню(по умолчанию)
                menu_background = Background('data/background_menu.png', [0, 0])
                self.screen.blit(menu_background.image, menu_background.rect)

                for i in range(3):

                    font = pygame.font.Font(None, 100)
                    text = font.render(buttons[i][0], True, pygame.Color('#FFE594'))  # текст
                    text_x = self.width // 2 - text.get_width() // 2 - 50
                    text_y = self.height // 3 - text.get_height() // 2 - 20 + i * 200
                    text_w = text.get_width()
                    text_h = text.get_height()
                    if len(button_location) != 4:  # избегаем перепись координат кнопок
                        button_location.append([text_x - 10, text_y - 10,
                                                text_w + 20, text_h + 20])  # запись занимаемых координат кнопкой

                    pygame.draw.rect(self.screen, (255, 150, 150), (text_x - 10, text_y - 10,
                                                                    text_w + 20, text_h + 20), 0)  # фон текста
                    if buttons[i][1] == 0:
                        pygame.draw.rect(self.screen, (10, 255, 0), (text_x - 10,
                                                                     text_y - 10,
                                                                     text_w + 20,
                                                                     text_h + 20), 4)  # безфокусная обводка текста
                    if buttons[i][1] == 1:
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
                if len(button_location) != 4:
                    button_location.append([text_x - 10, text_y - 10, text_w + 20, text_h + 20])
                if buttons[3][1] == 0:
                    pygame.draw.rect(self.screen, (255, 50, 50), (text_x - 10, text_y - 10,
                                                                  text_w + 20, text_h + 20), 0)
                elif buttons[3][1] == 1:
                    pygame.draw.rect(self.screen, (50, 50, 255), (text_x - 10, text_y - 10,
                                                                  text_w + 20, text_h + 20), 0)

                self.screen.blit(text, (text_x, text_y))

            if self.selected_screen == 'NewGameScreen':
                pass

            if self.selected_screen == 'Desktop':
                pass

            if self.selected_screen == 'Site':
                pass

            pygame.display.flip()
            clock.tick(100)

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


def draw_main_menu():  # перенести сюда простыню из app_running
    pass


def starting_screen():  # здесь будет рисоваться стартовый экран
    pass


def desktop_screen():  # здесь будет рисоваться "рабочий" стол
    pass


if __name__ == '__main__':
    app = SellAndGive()
