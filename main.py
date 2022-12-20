import pygame


class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        from win32api import GetSystemMetrics
        win_x = GetSystemMetrics(0)
        win_y = GetSystemMetrics(1)
        del GetSystemMetrics
        self.screen = pygame.display.set_mode(size=(win_x, win_y), flags=0)
        self.image = pygame.transform.scale(pygame.image.load('resource\\background.png'), (win_x, win_y))
        del win_x, win_y
        self.screen.blit(self.image, (0, 0))
        pygame.display.set_caption("WOWTCG")
        pygame.display.update()

    def start(self):
        pygame.time.Clock().tick(60)
        self.screen.blit(self.image, (0, 0))
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                self.main_loop()
                return 1
            else:
                del i
                return 0

    def main_loop(self):
        while True:
            pygame.time.Clock().tick(60)
            self.screen.fill((0, 0, 0))
            pygame.display.update()


if __name__ == '__main__':
    game = main()
    status = 0
    while status != 1:
        status = game.start()
