import pygame
import os
import sys

pygame.init()


def clear_and_load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

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


# ПРИНЦИП РАБОТЫ КЛАССА
# 1) берет clear_image.png, делает прозрачным
# 2) создает текст и ужимает прозрачный фон до размера текста
# 3) наносит текст на фон
class Button(pygame.sprite.Sprite):

    # name = текст кнопки,
    # coords = (x, y) положение кнопки,
    # color = (любой формат) цвет текста, можно указать None,
    # *group = группировка для кнопки
    def __init__(self, name, coords, color, *group):
        super().__init__(*group)

        if color is None:
            color = '#FFE594'
        font = pygame.font.Font('text_fonts/start_shr.ttf', 100)
        text_surface = font.render(name, True, pygame.Color(color))

        self.name = name
        self.tracing = False
        self.selected = False

        self.image = clear_and_load_image('clear_image.png', -1)
        self.coords = coords
        self.image = pygame.transform.scale(self.image, text_surface.get_size())
        self.image.blit(text_surface, (0, 0))
        self.size = self.image.get_width(), self.image.get_height()
        self.rect = coords

    def clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.coords[0] <= x <= self.coords[0] + self.image.get_rect()[2] and \
                self.coords[1] <= y <= self.coords[1] + self.image.get_rect()[3]:
            return True
        return False
