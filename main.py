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
        self.win_x = GetSystemMetrics(0)
        self.win_y = GetSystemMetrics(1)
        del GetSystemMetrics
        self.screen = pygame.display.set_mode(size=(self.win_x, self.win_y), flags=0)
        self.image = pygame.transform.scale(pygame.image.load('resource\\background.png'), (self.win_x, self.win_y))

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

        self.win_rule = win_rule(self)

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
        if self.win_rule.activate:
            self.win_rule.draw()

        self.screen.blit(self.mouse, mouse_pos)
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
                self.check_main_button(mouse_pos)
                self.check_win_rule_button(mouse_pos)

    def check_main_button(self, mouse_pos):
        if self.check_button(self.button_rule.rect, mouse_pos):
            self.win_rule.activate = True
            self.button_rule.activate = False

    def check_win_rule_button(self, mouse_pos):
        if self.check_button(self.win_rule.exit_rect, mouse_pos):
            self.win_rule.activate = False
            self.button_rule.activate = True
        if self.win_rule.activate:
            if self.check_button(self.win_rule.button_up.rect, mouse_pos):
                self.win_rule.page -= 1
                if self.win_rule.page == 0:
                    self.win_rule.page = 32
                self.win_rule.update_image()
        if self.check_button(self.win_rule.button_down.rect, mouse_pos):
            self.win_rule.page += 1
            if self.win_rule.page == 32:
                self.win_rule.page = 1
                self.win_rule.update_image()

    @staticmethod
    def check_button(rect, mouse_pos) -> bool:
        if rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class Button:
    def __init__(self, game, message: str, pos: tuple):
        self.screen = game.screen
        self.width, self.height = 175, 50
        self.button_color = (119, 136, 153)
        self.font_color = (0, 0, 0)
        self.font = pygame.font.Font('resource\\font.ttf', 45)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (pos[0], pos[1])
        self.message = message

        self.activate = True

        self.msg()

    def msg(self):
        self.image = self.font.render(self.message, True, self.font_color, self.button_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.image, self.image_rect)


class win_rule:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = game.win_x - 200
        self.height = game.win_y - 100
        self.bgc = (100, 150, 235)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.font = pygame.font.Font(None, 45)

        self.exit_rect = pygame.Rect(0, 0, 50, 50)
        self.exit_rect.center = self.rect.topright

        self.page = 1

        self.activate = False

        self.update_image()
        self.create_button(game)

    def update_image(self):
        self.image = pygame.image.load(f"resource\\rule\\{self.page}.jpg")
        self.image = pygame.transform.scale(self.image, (self.width - 20, self.height - 10))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.screen_rect.center

        self.exit_image = self.font.render('X', True, (255, 100, 100), (75, 125, 210))

    def create_button(self, game):
        self.button_up = Button(game, '上一页', self.rect.bottomleft)
        self.button_down = Button(game, '下一页', self.rect.bottomright)
        pass

    def draw(self):
        self.screen.fill(self.bgc, self.rect)
        self.screen.blit(self.image, self.image_rect)
        pygame.draw.circle(self.screen, (75, 125, 210), self.exit_rect.center, 30, 30)
        self.screen.blit(self.exit_image, (self.exit_rect.x + 10, self.exit_rect.y + 10))

        self.button_up.draw()
        self.button_down.draw()


if __name__ == '__main__':
    game = main()
    status = 0
    while status != 1:
        status = game.start()
    game.main_loop()
