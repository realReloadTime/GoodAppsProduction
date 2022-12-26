import pygame
import os
import sys

pygame.init()


def clear_and_load_image(name, colorkey=None):
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


class Button(pygame.sprite.Sprite):
    def __init__(self, name, coords, *group):
        super().__init__(*group)
        self.name = name
        self.image = clear_and_load_image('clear_image.png', -1)
        self.coords = coords
        font = pygame.font.Font('data/start_shr.ttf', 100)
        text_surface = font.render(name, True, pygame.Color('#FFE594'))
        pygame.transform.scale(self.image, text_surface.get_size())
        self.image.blit(text_surface, (0, 0))
        self.rect = coords

    def clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.coords[0] <= x <= self.coords[0] + self.rect[0] and\
           self.coords[1] <= y <= self.coords[1] + self.rect[1]:
            return True
        return False
