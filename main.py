import pygame
from tkinter import messagebox
from time import perf_counter


class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()

        from win32api import GetSystemMetrics
        win_x = GetSystemMetrics(0)
        win_y = GetSystemMetrics(1)
        del GetSystemMetrics
        self.screen = pygame.display.set_mode(size=(win_x, win_y), flags=0)
        self.image = pygame.transform.scale(pygame.image.load('resource\\background.png'), (win_x, win_y))
        del win_x, win_y

        messagebox.showinfo(title='开始！', message='关闭这个弹窗，开始载入游戏！')
        start = perf_counter()

        pygame.mouse.set_visible(False)
        self.screen.blit(self.image, (0, 0))
        pygame.display.set_caption("WOWTCG")
        pygame.display.update()

        self.mouse = pygame.image.load('resource\\mouse.png')
        self.mouse.set_colorkey((255, 255, 255))
        pygame.mixer.music.load('resource\\pop.wav')
        pygame.mixer.music.set_volume(0.3)

        messagebox.showinfo(title='好耶', message=f'加载完成,用了{(perf_counter() - start):.3f}秒!\n关掉弹窗再点一下就进去咯')


    def start(self) -> 0 or 1:
        pygame.time.Clock().tick(60)
        self.screen.blit(self.image, (0, 0))
        pygame.display.update()
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                return 1
            else:
                del i
                return 0

    def main_loop(self):
        while True:
            pygame.time.Clock().tick(60)
            self.create_object()
            self.display()
            self.check_event()

    def display(self):
        self.screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rule.rect.collidepoint(mouse_pos):
            self.button_rule.button_color = (176, 196, 222)
        else:
            self.button_rule.button_color = (119, 136, 153)
        self.button_rule.msg()
        self.button_rule.draw()

        self.screen.blit(self.mouse, (mouse_pos))
        pygame.display.update()

    def create_object(self):
        self.button_rule = Button(self, '规则', (200, 50))

    def check_event(self):
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_ESCAPE:
                    pygame.quit()
                    from sys import exit
                    exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.play()
                mouse_pos = pygame.mouse.get_pos()
                if self.check_button(self.button_rule, mouse_pos):
                    messagebox.showinfo(title='提示', message='我知道你点按钮了，但是程序员还没写内容呢')

    @staticmethod
    def check_button(button, mouse_pos) -> bool:
        if button.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class Button:
    def __init__(self, game, msg: str, pos: tuple):
        self.screen = game.screen
        self.width, self.height = 200, 50
        self.button_color = (119, 136, 153)
        self.font_color = (0, 0, 0)
        self.font = pygame.font.Font('resource\\font.ttf', 45)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (pos[0], pos[1])
        self.message = msg

    def msg(self):
        self.image = self.font.render(self.message, True, self.font_color, self.button_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.image, self.image_rect)


if __name__ == '__main__':
    game = main()
    status = 0
    while status != 1:
        status = game.start()
    game.main_loop()
