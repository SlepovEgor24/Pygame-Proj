import sys
import os
import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 60
VOLUME_FILE = 'files\\volume.txt'
FONT = 'EpilepsySans.ttf'
FONT_SIZE = 44


class Buttons:
    def __init__(self, x, y, width, height, img, text, img_true=None, sound=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.img = load_image(img, '\\main')
        self.img = pygame.transform.scale(self.img, (width, height))
        self.img_true = self.img
        if img_true:
            self.img_true = load_image(img_true, '\\main')
            self.img_true = pygame.transform.scale(self.img_true, (width, height))
        self.rect = self.img.get_rect(topleft=(x, y))
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(load_sounds(sound))
        self.cursor_on_button = False
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        if self.cursor_on_button:
            current_img = self.img_true
        else:
            current_img = self.img
        screen.blit(current_img, self.rect.topleft)
        font = pygame.font.Font(FONT, FONT_SIZE)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_cursor(self, mouse_pos):
        x = mouse_pos[0] - self.rect.left
        y = mouse_pos[1] - self.rect.top
        if 0 <= x < self.rect.width and 0 <= y < self.rect.height:
            self.cursor_on_button = self.mask.get_at((x, y))
        else:
            self.cursor_on_button = False

    def mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.check_cursor(pygame.mouse.get_pos())
            if self.cursor_on_button:
                if self.sound:
                    self.sound.play()
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class Slider:
    def __init__(self, x, y, length, min_value, max_value, value, img):
        self.x = x
        self.y = y
        self.length = length
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.slider_moving = False
        self.img_sound = load_image(img, '\\main')
        self.img_sound = pygame.transform.scale(self.img_sound, (100, 60))
        self.slider = load_image('polzunok.png', '\\main')
        self.slider = pygame.transform.scale(self.slider, (30, 30))

    def draw(self, screen):
        pygame.draw.line(screen, (255, 255, 255), (self.x + 50, self.y + 25),
                         (self.x + self.length + 50, self.y + 25), 5)
        position = self.x + 50 + (self.value - self.min_value) / (
                self.max_value - self.min_value) * self.length
        screen.blit(self.slider, (int(position) - self.slider.get_width() // 2,
                                  self.y + 25 - self.slider.get_height() // 2))
        screen.blit(self.img_sound, (self.x - 30, self.y))

    def check_cursor(self, mouse_pos):
        position = self.x + 50 + (self.value - self.min_value) / (
                self.max_value - self.min_value) * self.length
        rect = self.slider.get_rect(center=(int(position), self.y + 25))
        return rect.collidepoint(mouse_pos)

    def mouse_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.check_cursor(event.pos):
                self.slider_moving = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_moving = False
        elif event.type == pygame.MOUSEMOTION and self.slider_moving:
            position = event.pos[0] - 50
            if position < self.x:
                position = self.x
            elif position > self.x + self.length:
                position = self.x + self.length
            self.value = self.min_value + (position - self.x) / self.length * (
                    self.max_value - self.min_value)
            pygame.mixer.music.set_volume(self.value / 100)


class SettingsMenu:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = main_background
        self.cursor = cursor
        self.value_slider = Slider(WINDOW_WIDTH / 2 - 120, 200, 200, 0, 100,
                                   pygame.mixer.music.get_volume() * 100, 'sound2.png')
        self.manual_button = Buttons(WINDOW_WIDTH / 2 - 100, 300, 200, 74, 'button.png', 'Manual',
                                     'button_true.png', 'close2.mp3')
        self.back_button = Buttons(WINDOW_WIDTH / 2 - 80, 400, 150, 50, 'back.png', '',
                                   'back_true.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, FONT_SIZE)
            text = font.render('Настройки', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_volume()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_sound.play()
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                if event.type == pygame.USEREVENT:
                    if event.button == self.back_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                    elif event.button == self.manual_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        ManualWindow(self.screen, self.main_background, self.cursor).run()
                self.value_slider.mouse_event(event)
                self.manual_button.mouse_event(event)
                self.back_button.mouse_event(event)

            self.value_slider.draw(self.screen)
            self.manual_button.check_cursor(pygame.mouse.get_pos())
            self.manual_button.draw(self.screen)
            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class ManualWindow:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = main_background
        self.cursor = cursor
        self.back_button = Buttons(WINDOW_WIDTH / 2 - (252 / 2), 600, 252, 74, 'back.png', '',
                                   'back_true.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, FONT_SIZE)
            text = font.render('Инструкция', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)
            instructions = [
                'Управление:',
                'W - Вперёд',
                'S - Назад',
                'A - Влево',
                'D - Вправо',
                'Escape - Назад/Пауза',
                'ЛКМ - Атака'
            ]
            for i, line in enumerate(instructions):
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (WINDOW_WIDTH / 2 - 200, 200 + i * 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == self.back_button:
                    Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_sound.play()
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                self.back_button.mouse_event(event)
            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class Play:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = main_background
        self.cursor = cursor
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))
        self.background = load_image('main.png', '\\main')
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons = []
        self.back_button = Buttons(
            WINDOW_WIDTH - 170, WINDOW_HEIGHT - 80, 160, 55,
            'back.png', '',
            'back_true.png', 'close2.mp3'
        )
        self.create_buttons()

    def create_buttons(self):
        part_width = WINDOW_WIDTH // 3
        for i in range(3):
            x = i * part_width + part_width // 2
            for j in range(5):
                y = (WINDOW_HEIGHT // 6) * (j + 1)
                button = Buttons(
                    x - 50,
                    y - 25,
                    100, 50,
                    'button.png', str(5 - j),
                    'button_true.png', 'close2.mp3'
                )
                self.buttons.append(button)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_sound.play()
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                if event.type == pygame.USEREVENT:
                    if event.button == self.back_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                self.back_button.mouse_event(event)
                for button in self.buttons:
                    button.mouse_event(event)
            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)
            for button in self.buttons:
                button.check_cursor(pygame.mouse.get_pos())
                button.draw(self.screen)
            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class Transition:
    def __init__(self, screen, width, height, max_fps):
        self.screen = screen
        self.width = width
        self.height = height
        self.max_fps = max_fps

    def transition(self):
        running = True
        level_transparency = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            surface = pygame.Surface((self.width, self.height))
            surface.fill((0, 0, 0))
            surface.set_alpha(level_transparency)
            level_transparency += 5
            self.screen.blit(surface, (0, 0))
            if level_transparency >= 100:
                level_transparency = 255
                running = False
            pygame.display.flip()
            clock.tick(self.max_fps)


def load_image(name, puth, colorkey=None):
    fullname = os.path.join(f'files{puth}', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображение "{fullname}" отсутствует')
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


def load_sounds(name):
    fullname = os.path.join('files', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f'Файл со звуком "{fullname}" отсутствует')
        sys.exit()
    return fullname


def save_volume():
    with open(VOLUME_FILE, 'w') as file:
        file.write(str(pygame.mixer.music.get_volume()))


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
icon = load_image('icon.png', '\\main')
pygame.display.set_icon(icon)
pygame.display.set_caption('Продержись!')
main_background = load_image('background (1).jpg', '\\main')
clock = pygame.time.Clock()
cursor = load_image('cursor.png', '\\main')
cursor = pygame.transform.scale(cursor, (22, 29))
pygame.mouse.set_visible(False)
pygame.mixer.music.load(load_sounds('main.mp3'))
pygame.mixer.music.play(-1)
try:
    with open(VOLUME_FILE, 'r') as file:
        volume = float(file.read())
        pygame.mixer.music.set_volume(volume)
except FileNotFoundError:
    volume = 0.5
    pygame.mixer.music.set_volume(volume)


def main():
    exit_button = Buttons(WINDOW_WIDTH / 2 - 97.5, 550, 195, 70, 'exit.png', '',
                          'exit_true2.png',
                          'close2.mp3')
    play_button = Buttons(WINDOW_WIDTH / 2 - 107, 430, 230, 135, 'play.png', '',
                          'play_true.png',
                          'close2.mp3')
    setting_button = Buttons(WINDOW_WIDTH - 100, 10, 68, 70, 'setting.png', '',
                             'setting_true.png',
                             'close2.mp3')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))
        font = pygame.font.Font(FONT, FONT_SIZE)
        text = font.render('Продержись 3 минуты!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_volume()
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.button == play_button:
                    Transition(screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    Play(screen, main_background, cursor).run()
                elif event.button == setting_button:
                    Transition(screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    SettingsMenu(screen, main_background, cursor).run()
                elif event.button == exit_button:
                    save_volume()
                    Transition(screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    running = False
                    pygame.quit()
                    sys.exit()
            for button in [play_button, setting_button, exit_button]:
                button.mouse_event(event)
        mouse_pos = pygame.mouse.get_pos()
        for button in [play_button, setting_button, exit_button]:
            button.check_cursor(pygame.mouse.get_pos())
            button.draw(screen)
        if pygame.mouse.get_focused():
            screen.blit(cursor, mouse_pos)
        pygame.display.flip()


if __name__ == '__main__':
    main()
