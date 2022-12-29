import pygame

pygame.init()


def label(text, location, font_name='text_fonts/start_shr.ttf', size=50, color='black'):
    font = pygame.font.Font(font_name, 100)
    text_surface = font.render(text, True, pygame.Color(color))
    return text_surface, text_surface.get_width() + location[0], text_surface.get_height() + location[1]