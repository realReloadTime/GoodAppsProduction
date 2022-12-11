import pygame
from win32api import GetSystemMetrics


class SellAndGive:
    def __init__(self):
        self.width_and_height = GetSystemMetrics(0), GetSystemMetrics(1)
        self.screen = pygame.display.set_mode(self.width_and_height)
        self.all_screens = ['MainMenu']
        self.selected_screen = self.all_screens[0]
        self.app_start()

    def app_start(self):
        pygame.init()

        pygame.display.set_caption('Продай и отдай')
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((31, 204, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.app_end()
                    running = False

            if not running:
                continue

            if self.selected_screen == 'MainMenu':
                menu_background = Background('background_menu.png', [0, 0])
                self.screen.blit(menu_background.image, menu_background.rect)

            pygame.display.flip()
            clock.tick(1)

    def app_end(self):  # saves all changes
        self.screen.fill((100, 100, 100))
        pygame.display.flip()
        pygame.quit()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


if __name__ == '__main__':
    app = SellAndGive()
