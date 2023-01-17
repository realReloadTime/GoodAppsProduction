import pygame

pygame.init()


# берет текст, расположение, название файла шрифта(необяз.), размер(необяз.), цвет(любой формат, необяз.)
# возвращает плоскость текста, координаты концов(по горизонтали и вертикали)
def label(text, location, font_name='start_shr.ttf', size=50, color='black'):
    if font_name is not None:
        font_name = 'text_fonts/' + font_name
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color(color))
    return text_surface, location, text_surface.get_width(), text_surface.get_height()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.w = w
        self.active_color, self.unactive_color = 'white', 'black'
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('black')
        self.text = text
        self.font_val = pygame.font.Font('text_fonts/button_shr.ttf', 32)
        self.txt_surface = self.font_val.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_color if self.active else self.unactive_color
        if event.type == pygame.KEYUP:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font_val.render(self.text, True, self.unactive_color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)