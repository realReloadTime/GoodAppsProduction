import pygame
import os
import sys


class Image(pygame.sprite.Sprite):  # преобразует файл изображения в формат, распознаваемый pygame
    def __init__(self, image_file, location=(0, 0), resize=False, resize_size=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        if resize:
            if all(resize_size):
                self.image = pygame.transform.scale(self.image, resize_size)
            else:
                self.image = pygame.transform.scale(self.image, (1920, 1080))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.coords[0] <= x <= self.coords[0] + self.image.get_rect()[2] and \
                self.coords[1] <= y <= self.coords[1] + self.image.get_rect()[3]:
            return True
        return False


class Icon(pygame.sprite.Sprite):
    def __init__(self, image_file, coords=(0, 0), *group):
        super().__init__(*group)
        self.coords = coords
        self.image = load_image(image_file, -1)
        self.tracing = False
        self.image = pygame.transform.scale(self.image, (220, 200))
        self.size = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.coords

    def clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.coords[0] <= x <= self.coords[0] + self.image.get_rect()[2] and \
                self.coords[1] <= y <= self.coords[1] + self.image.get_rect()[3]:
            return True
        return False


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