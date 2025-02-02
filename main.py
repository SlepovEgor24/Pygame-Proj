import sys
import os
import pygame
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MAX_FPS = 60
VOLUME_FILE = 'files\\volume.txt'
VOLUME2_FILE = 'files\\volume2.txt'
LEVEL_STATUS = 'files\\levelstatus.txt'
FONT = 'files\\EpilepsySans.ttf'
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
    def __init__(self, x, y, length, min_value, max_value, value, img, sound_object=None):
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
        self.sound_object = sound_object

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
            if self.sound_object:
                self.sound_object.set_volume(self.value / 100)


pixsel = WINDOW_HEIGHT // 360
BONFIREEVENT = pygame.USEREVENT + 1
TEMPEVENT = pygame.USEREVENT + 2
MOBEVENT = pygame.USEREVENT + 3


def level(difficult, music):
    global BONFIREEVENT, TEMPEVENT, MOBEVENT
    pygame.time.set_timer(BONFIREEVENT, difficult[0] * 15 * 10 * 10 * 2)
    pygame.time.set_timer(TEMPEVENT, difficult[0] * 25)
    pygame.time.set_timer(MOBEVENT, difficult[0] * 25 * 10 * 10 * 4)
    all_sprites = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    list_with_objects = []

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.x, self.y = x, y
            self.k = 0
            self.columns = columns
            self.rows = rows
            self.run = [True, True, True, True]
            self.hp = 4
            self.update()

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self, *args):
            self.rect.x = self.x - player.x + 580
            self.rect.y = self.y - player.y + 310
            self.k += 1
            if self.k == 12 and True in self.run:
                self.cur_frame = (self.cur_frame + 1) % self.rows + self.run.index(
                    True) * self.columns
                self.image = self.frames[self.cur_frame]
                self.k = 0
            if self.x - player.x < 0:
                self.vx = 199
                self.run[2] = True
                self.run[1] = False
            elif self.x - player.x > 0:
                self.vx = -199
                self.run[2] = False
                self.run[1] = True
            else:
                self.vx = 0
                self.run[2] = False
                self.run[1] = False
            if self.y - player.y < 0:
                self.vy = 199
                self.run[0] = True
                self.run[3] = False
            elif self.y - player.y > 0:
                self.vy = -199
                self.run[0] = False
                self.run[3] = True
            else:
                self.vy = 0
                self.run[0] = False
                self.run[3] = False
            self.x += self.vx // FPS
            self.y += self.vy // FPS
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and player.axe
                    and abs(self.rect.x - 320 * pixsel) < 120 * pixsel and
                    abs(self.rect.y - 200 * pixsel) < 120 * pixsel):
                self.hp -= 1
                self.x -= self.vx
                self.y -= self.vy
            if abs(self.rect.x - 320 * pixsel) < 50 * pixsel and abs(
                    self.rect.y - 200 * pixsel) < 50 * pixsel:
                player.hp -= 0.1
            if self.hp <= 0:
                all_sprites.remove(self)
                del self

    class Map:
        def __init__(self):
            self.x = 10000
            self.y = 10000

    class Snow(pygame.sprite.Sprite):
        image = load_image("snow.png", "\\world\\map")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            global pixsel
            self.image = Snow.image
            self.image = pygame.transform.scale(self.image, (690, 360))
            self.rect = self.image.get_rect()
            self.x, self.y = x, y
            self.rect.x = 0
            self.rect.y = 0

        def update(self, *args):
            self.rect.x = self.x - player.x % 690
            self.rect.y = self.y - player.y % 360

    class Player(pygame.sprite.Sprite):  # Класс игрока
        image_w0 = load_image("forester_w0.png", "\\world\\player")
        image_w0 = pygame.transform.scale(image_w0, (60 * pixsel, 60 * pixsel))
        image_e0 = load_image("forester_e0.png", "\\world\\player")
        image_e0 = pygame.transform.scale(image_e0, (60 * pixsel, 60 * pixsel))
        image_s0 = load_image("forester_s0.png", "\\world\\player")
        image_s0 = pygame.transform.scale(image_s0, (60 * pixsel, 60 * pixsel))
        image_n0 = load_image("forester_n0.png", "\\world\\player")
        image_n0 = pygame.transform.scale(image_n0, (60 * pixsel, 60 * pixsel))
        image_w1 = load_image("forester_w1.png", "\\world\\player")
        image_w1 = pygame.transform.scale(image_w1, (60 * pixsel, 60 * pixsel))
        image_e1 = load_image("forester_e1.png", "\\world\\player")
        image_e1 = pygame.transform.scale(image_e1, (60 * pixsel, 60 * pixsel))
        image_s1 = load_image("forester_s1.png", "\\world\\player")
        image_s1 = pygame.transform.scale(image_s1, (60 * pixsel, 60 * pixsel))
        image_n1 = load_image("forester_n1.png", "\\world\\player")
        image_n1 = pygame.transform.scale(image_n1, (60 * pixsel, 60 * pixsel))
        image_w2 = load_image("forester_w2.png", "\\world\\player")
        image_w2 = pygame.transform.scale(image_w2, (60 * pixsel, 60 * pixsel))
        image_e2 = load_image("forester_e2.png", "\\world\\player")
        image_e2 = pygame.transform.scale(image_e2, (60 * pixsel, 60 * pixsel))
        image_s2 = load_image("forester_s2.png", "\\world\\player")
        image_s2 = pygame.transform.scale(image_s2, (60 * pixsel, 60 * pixsel))
        image_n2 = load_image("forester_n2.png", "\\world\\player")
        image_n2 = pygame.transform.scale(image_n2, (60 * pixsel, 60 * pixsel))

        def __init__(self, *group):
            super().__init__(*group)
            global pixsel
            self.image = Player.image_w2
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.axe = False
            self.run = [0, 0, 0, 0]
            self.x, self.y = 0, 0
            self.rect.x = WINDOW_WIDTH // 2
            self.rect.y = WINDOW_HEIGHT // 2
            self.wood = False
            self.hp = 100
            self.temp = 50
            self.counter = 1

        def reset_movement(self):
            self.run = [0, 0, 0, 0]

        def update(self, *args):
            global TEMPEVENT
            if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'w':
                self.run[0] = 0
            if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'w':
                self.run[0] = 1
                if self.wood:
                    self.image = Player.image_n1
                elif self.axe:
                    self.image = Player.image_n0
                else:
                    self.image = Player.image_n2
            if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 's':
                self.run[1] = 0
            if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 's':
                self.run[1] = 1
                if self.wood:
                    self.image = Player.image_s1
                elif self.axe:
                    self.image = Player.image_s0
                else:
                    self.image = Player.image_s2
            if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'd':
                self.run[2] = 0
            if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'd':
                self.run[2] = 1
                if self.wood:
                    self.image = Player.image_e1
                elif self.axe:
                    self.image = Player.image_e0
                else:
                    self.image = Player.image_e2
            if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'a':
                self.run[3] = 0
            if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'a':
                self.run[3] = 1
                if self.wood:
                    self.image = Player.image_w1
                elif self.axe:
                    self.image = Player.image_w0
                else:
                    self.image = Player.image_w2
            if args and args[0].type == pygame.KEYDOWN and args[0].key == 1073742049:
                if self.wood:
                    self.wood = False
                    self.image = Player.image_e0
                    Wood(self.x + 50, self.y + 650, all_sprites)
            sprites = list()
            for sprite in all_sprites:
                if sprite != self and abs(sprite.x - player.x) < 1280 and abs(
                        sprite.y - player.y) < 720:
                    sprites.append(sprite)
            if self.run[0] == 1:
                self.y -= v // FPS
                for sprite in sprites:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.y += v // FPS * 2
                        self.run[0] = 0
                        break
            if self.run[1] == 1:
                self.y += v // FPS
                for sprite in sprites:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.y -= v // FPS * 2
                        self.run[1] = 0
                        break
            if self.run[2] == 1:
                self.x += v // FPS
                for sprite in sprites:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.x -= v // FPS * 2
                        self.run[2] = 0
                        break
            if self.run[3] == 1:
                self.x -= v // FPS
                for sprite in sprites:
                    if pygame.sprite.collide_mask(self, sprite):
                        self.x += v // FPS * 2
                        self.run[3] = 0
                        break
            if args and args[0].type == TEMPEVENT:
                if (abs(bonfire.rect.x - 320 * pixsel) < 80 * pixsel and
                        abs(bonfire.rect.y - 180 * pixsel) < 80 * pixsel and bonfire.run > 1):
                    self.temp = min(self.temp + bonfire.run, 100)
                else:
                    if self.temp == 0:
                        self.hp = max(self.hp - 1.25, 0)
                        if self.counter == 5:
                            pygame.mixer.Sound(load_sounds('took_damage.mp3')).play()
                            self.counter = 0
                        self.counter += 1
                    else:
                        self.temp = max(self.temp - 1.25, 0)

    class ChristmasTree(pygame.sprite.Sprite):  # класс блока - елки
        image = load_image("tree.png", "\\world\\blocks\\tree")
        image2 = load_image("stump.png", "\\world\\blocks\\tree")

        def __init__(self, objects, *group):
            super().__init__(*group)
            global pixsel
            self.image = ChristmasTree.image
            self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.sound_broke_tree = pygame.mixer.Sound(load_sounds('hit.mp3'))
            while True:
                x = random.randrange(int(-0.7 * map.x), int(0.7 * map.x))
                y = random.randrange(int(-0.7 * map.y), int(0.7 * map.y))
                if x < -500 or x > 500 or y < -500 or y > 500 + self.rect.h and not dist_between_objects(
                        x, y, objects, 30):
                    self.x = x
                    self.y = y
                    break
            self.chopped = False

        def update(self, *args):
            self.rect.x = self.x - player.x + 300 * pixsel
            self.rect.y = self.y - player.y - 200 * pixsel
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos)
                    and abs(self.x - player.x) < 300 and abs(self.y - player.y - 500) < 230
                    and not self.chopped and player.axe):
                if player.wood:  # Если игрок держит бревно, сбрасываем его.
                    player.wood = False
                    player.image = Player.image_e0
                    Wood(player.x, player.y + self.rect.h * 2 + 10, all_sprites)
                self.sound_broke_tree.play()
                self.image = ChristmasTree.image2
                self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
                self.chopped = True
                self.mask = pygame.mask.from_surface(self.image)
                Wood(self.x + self.rect.w // 2, self.y + self.rect.h // 2, all_sprites)

    class Wood(pygame.sprite.Sprite):  # класс блока - елки
        image = load_image("wood.png", "\\world\\blocks\\tree")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            global pixsel
            self.image = Wood.image
            self.image = pygame.transform.scale(self.image, (60 * pixsel, 60 * pixsel))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.x, self.y = x, y
            self.update()

        def update(self, *args):
            self.rect.x = self.x - player.x + 300 * pixsel
            self.rect.y = self.y - player.y - 200 * pixsel
            if pygame.sprite.collide_mask(self, player) and not player.wood:
                player.wood = True
                player.image = Player.image_e1
                all_sprites.remove(self)
                del self

    class Axe(pygame.sprite.Sprite):  # класс блока - топора
        image = load_image("axe.png", "\\world\\blocks")

        def __init__(self, *group):
            super().__init__(*group)
            global pixsel
            self.image = Axe.image
            self.image = pygame.transform.scale(self.image, (60 * pixsel, 60 * pixsel))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.x = random.randint(200, 300)
            self.y = random.randint(200, 300)

        def update(self, *args):
            self.rect.x = self.x - player.x + 690
            self.rect.y = self.y - player.y + 360
            if pygame.sprite.collide_mask(self, player):
                player.axe = True
                player.image = Player.image_e0
                all_sprites.remove(self)
                del self

    class Ruins(pygame.sprite.Sprite):
        image2 = load_image("2.png", "\\sprites\\okr1\\2 Objects\\Ruins")
        image3 = load_image("3.png", "\\sprites\\okr1\\2 Objects\\Ruins")
        image4 = load_image("4.png", "\\sprites\\okr1\\2 Objects\\Ruins")
        image5 = load_image("5.png", "\\sprites\\okr1\\2 Objects\\Ruins")

        def __init__(self, objects, *group):
            super().__init__(*group)
            z = random.randrange(2, 6)
            if z == 2:
                self.image = Ruins.image2
            elif z == 3:
                self.image = Ruins.image3
            elif z == 4:
                self.image = Ruins.image4
            elif z == 5:
                self.image = Ruins.image5
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (5 * self.rect.w, 5 * self.rect.h))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            while True:
                x = random.randrange(int(-map.x), int(map.x))
                y = random.randrange(int(-map.y), int(map.y))
                if x < -380 or x > 380 or y < -380 or y > 380 + self.rect.h and not dist_between_objects(
                        x, y, objects, 30):
                    self.x = x
                    self.y = y
                    break

        def update(self, *args):
            self.rect.x = self.x - player.x + 690
            self.rect.y = self.y - player.y + 360

    class Rocks(pygame.sprite.Sprite):
        image6 = load_image("6.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")
        image1 = load_image("1.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")
        image2 = load_image("2.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")
        image3 = load_image("3.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")
        image4 = load_image("4.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")
        image5 = load_image("5.png", "\\sprites\\okruzhenie_9\\2 Objects\\Rocks")

        def __init__(self, objects, *group):
            super().__init__(*group)
            z = random.randrange(2, 6)
            if z == 1:
                self.image = Rocks.image1
            elif z == 3:
                self.image = Rocks.image3
            elif z == 4:
                self.image = Rocks.image4
            elif z == 5:
                self.image = Rocks.image5
            elif z == 2:
                self.image = Rocks.image2
            elif z == 6:
                self.image = Rocks.image6
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (5 * self.rect.w, 5 * self.rect.h))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            while True:
                x = random.randrange(int(-map.x), int(map.x))
                y = random.randrange(int(-map.y), int(map.y))
                if x < -380 or x > 380 or y < -380 or y > 380 + self.rect.h and not dist_between_objects(
                        x, y, objects, 30):
                    self.x = x
                    self.y = y
                    break

        def update(self, *args):
            self.rect.x = self.x - player.x + 300 * pixsel
            self.rect.y = self.y - player.y - 200 * pixsel

    class Bonfire(pygame.sprite.Sprite):
        image_0 = load_image("bonfire0.png", "\\world\\blocks\\bonfire")
        image_0 = pygame.transform.scale(image_0, (30 * pixsel, 30 * pixsel))
        image_1 = load_image("bonfire1.png", "\\world\\blocks\\bonfire")
        image_1 = pygame.transform.scale(image_1, (30 * pixsel, 30 * pixsel))
        image_2 = load_image("bonfire2.png", "\\world\\blocks\\bonfire")
        image_2 = pygame.transform.scale(image_2, (30 * pixsel, 30 * pixsel))
        image_3 = load_image("bonfire3.png", "\\world\\blocks\\bonfire")
        image_3 = pygame.transform.scale(image_3, (30 * pixsel, 30 * pixsel))
        image_4 = load_image("bonfire4.png", "\\world\\blocks\\bonfire")
        image_4 = pygame.transform.scale(image_4, (30 * pixsel, 30 * pixsel))
        image_5 = load_image("bonfire5.png", "\\world\\blocks\\bonfire")
        image_5 = pygame.transform.scale(image_5, (30 * pixsel, 30 * pixsel))

        def __init__(self, *group):
            super().__init__(*group)
            global pixsel
            self.image = Bonfire.image_3
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.run = 3
            self.x, self.y = 0, 400 * 2
            self.counter = 1

        def update(self, *args):
            global BONFIREEVENT, TEMPEVENT
            self.rect.x = self.x - player.x + 300 * pixsel
            self.rect.y = self.y - player.y - 200 * pixsel
            watch = False
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                    args[0].pos) and player.wood
                    and abs(self.rect.x - 320 * pixsel) < 60 * pixsel and
                    abs(self.rect.y - 200 * pixsel) < 60 * pixsel and self.run < 5):
                player.wood = False
                player.image = Player.image_e0
                self.run = min(self.run + 1, 5)
                watch = True
            if args and args[0].type == BONFIREEVENT:
                self.run = max(self.run - 1, 0)
                watch = True
            if watch:
                if self.run == 0:
                    self.image = Bonfire.image_0
                    self.mask = pygame.mask.from_surface(self.image)
                elif self.run == 1:
                    self.image = Bonfire.image_1
                    self.mask = pygame.mask.from_surface(self.image)
                elif self.run == 2:
                    self.image = Bonfire.image_2
                    self.mask = pygame.mask.from_surface(self.image)
                elif self.run == 3:
                    self.image = Bonfire.image_3
                    self.mask = pygame.mask.from_surface(self.image)
                elif self.run == 4:
                    self.image = Bonfire.image_4
                    self.mask = pygame.mask.from_surface(self.image)
                elif self.run == 5:
                    self.image = Bonfire.image_5
                    self.mask = pygame.mask.from_surface(self.image)
            if args and args[0].type == TEMPEVENT and (
                    abs(self.rect.x - 340 * pixsel) < 5 * pixsel and
                    abs(self.rect.y - 210 * pixsel) < 5 * pixsel):
                player.hp = max(player.hp - 4 * bonfire.run, 0)
                if self.counter == 3:
                    pygame.mixer.Sound(load_sounds('took_damage.mp3')).play()
                    self.counter = 0
                self.counter += 1
                player.temp = min(player.temp + 4 * bonfire.run, 100)

    # Начало работы программы
    running = True
    time = 0
    map = Map()
    bonfire = Bonfire(all_sprites)
    player = Player(all_sprites)
    Axe(all_sprites)
    for i in range(5 * 100):
        tree = ChristmasTree(list_with_objects, all_sprites)
        list_with_objects.append(tree)
    for i in range(60):
        ruin = Ruins(list_with_objects, all_sprites)
        list_with_objects.append(ruin)
    for i in range(80):
        rock = Rocks(list_with_objects, all_sprites)
        list_with_objects.append(rock)
    Snow(0, 0, wall)
    Snow(690, 0, wall)
    Snow(0, 360, wall)
    Snow(690, 360, wall)
    Snow(0, 720, wall)
    Snow(690, 720, wall)
    Snow(1280, 0, wall)
    Snow(1280, 360, wall)
    Snow(1280, 720, wall)
    FPS = 100
    v = 200
    clock = pygame.time.Clock()
    while running:
        wall.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    value = PauseWindow(screen, 'les.jpg', cursor, music, player).run()
                    if value:
                        music.stop()
                        pygame.mixer.music.unpause()
                        return
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYDOWN:
                all_sprites.update(event)
            if event.type == pygame.KEYUP:
                all_sprites.update(event)
            if event.type == BONFIREEVENT or event.type == TEMPEVENT:
                all_sprites.update(event)
            if event.type == MOBEVENT:
                if random.randint(0, 2) == 1:
                    while True:
                        x = random.randrange(player.x - 1280, player.x + 1280)
                        y = random.randrange(player.y - 720, player.y + 720)
                        if x > player.x + 690 or x < player.x - 690 or y > player.y + 360 or y < player.y - 360:
                            break
                    AnimatedSprite(load_image("Boar_Move.png",
                                              "\\sprites\\vragi_6\\Monster Pack 21 (Bovine)\\Spritesheets\\Updated Boar"),
                                   6, 4, x, y)

        screen.fill((0, 0, 0))
        clock.tick(FPS)
        wall.draw(screen)
        sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.rect.y + sprite.rect.h)
        for sprite in sorted_sprites:
            if abs(sprite.x - player.x) < 1280 * 2 and abs(
                    sprite.y - player.y) < 720 * 2 + sprite.rect.h:
                screen.blit(sprite.image, sprite.rect)
        all_sprites.update()
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, 80, 50), 0)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 80, 50), 5)
        pygame.draw.rect(screen, (255, 255, 0), (80, 0, 90, 50), 0)
        pygame.draw.rect(screen, (0, 0, 0), (80, 0, 90, 50), 5)
        text_surface = pygame.font.Font(FONT, 25).render(
            f' {int(player.hp)}       {int(player.temp)}', True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
        time += 1

        # Форматирование времени
        minutes = time // FPS // 60
        seconds = (time // FPS) % 60
        formatted_time = f'{minutes}:{seconds:02}'
        pygame.display.set_caption(f'Продержался {formatted_time}')

        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()
        if player.hp <= 0:
            # Проигрыш
            return 2
        if time // FPS // 60 >= 3:
            # Победа
            return 3


class LevelWindow:
    def __init__(self, screen, main_background, cursor, music, difficulty):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
        self.cursor = cursor
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))
        self.music = music
        self.sound_win = pygame.mixer.Sound(load_sounds('inecraft_levelu.mp3'))
        self.sound_lose = pygame.mixer.Sound(load_sounds('death.mp3'))
        self.difficulty = difficulty
        try:
            with open(VOLUME2_FILE, 'r') as file:
                volume = float(file.read())
                self.music.set_volume(volume)
        except FileNotFoundError:
            volume = 0.5
            self.music.set_volume(volume)

        self.music.play(-1)
        pygame.mixer.music.pause()

    def run(self):
        level_passed = level([self.difficulty], self.music)
        pygame.display.set_caption(f'Продержись!')
        if level_passed == 3:
            self.sound_win.play()
            win_window = WinLoseWindow(self.screen, 'les.jpg', self.cursor, self.music,
                                       [self.difficulty], True)
            restart = win_window.run()
            self.unlock_next_level()
            if restart:
                self.run()
            else:
                self.music.stop()
                pygame.mixer.music.unpause()
                Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                return
        elif level_passed == 2:
            self.sound_lose.play()
            lose_window = WinLoseWindow(self.screen, 'les.jpg', self.cursor, self.music,
                                        [self.difficulty], False)
            restart = lose_window.run()
            if restart:
                self.run()
            else:
                self.music.stop()
                pygame.mixer.music.unpause()
                Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                return
        self.music.stop()
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            self.screen.blit(self.cursor, (x - 2, y - 2))
        pygame.display.flip()

    def unlock_next_level(self):
        level_status = load_level_status()
        current_level_index = 5 - self.difficulty
        if current_level_index < len(level_status) - 1:
            level_status[current_level_index + 1] = True
            save_level_status(level_status)


class WinLoseWindow:
    def __init__(self, screen, main_background, cursor, music, difficulty, value):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
        self.cursor = cursor
        self.music = music
        self.difficulty = difficulty
        self.value = value
        self.exit_button = Buttons(WINDOW_WIDTH / 2 - 100, 400, 200, 74, 'exit.png', '',
                                   'exit_true2.png', 'close2.mp3')
        self.restart_button = Buttons(WINDOW_WIDTH / 2 - 125, 300, 290, 74, 'button.png',
                                      'Пройти заново',
                                      'button_true.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, FONT_SIZE)
            if self.value:
                text = font.render('Вы выиграли!', True, (255, 255, 255))
                text2 = font.render('Вам удалось продержаться 3 минуты!', True, (255, 255, 255))
            else:
                text = font.render(f'Вы проиграли!', True, (255, 255, 255))
                text2 = font.render(f'Вам не удалось продержаться 3 минуты!', True,
                                    (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
            text_rect2 = text2.get_rect(center=(WINDOW_WIDTH / 2, 150))
            self.screen.blit(text, text_rect)
            self.screen.blit(text2, text_rect2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.button == self.exit_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return False
                    elif event.button == self.restart_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        self.music.stop()
                        self.music.play()
                        return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_sound.play()
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return False
                self.exit_button.mouse_event(event)
                self.restart_button.mouse_event(event)
            self.exit_button.check_cursor(pygame.mouse.get_pos())
            self.exit_button.draw(self.screen)
            self.restart_button.check_cursor(pygame.mouse.get_pos())
            self.restart_button.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class PauseWindow:
    def __init__(self, screen, main_background, cursor, music, player):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
        self.cursor = cursor
        self.music = music
        self.player = player
        self.resume_button = Buttons(WINDOW_WIDTH / 2 - 120, 300, 250, 74, 'button.png',
                                     'Продолжить', 'button_true.png', 'close2.mp3')
        self.back_button = Buttons(WINDOW_WIDTH / 2 - 100, 400, 200, 74, 'exit.png', '',
                                   'exit_true2.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))
        self.value_slider = Slider(WINDOW_WIDTH / 2 - 120, 200, 200, 0, 100,
                                   self.music.get_volume() * 100, 'sound2.png', self.music)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, FONT_SIZE)
            text = font.render('Пауза', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_volume(VOLUME2_FILE, self.music.get_volume())
                    pygame.mixer.music.unpause()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.button == self.resume_button:
                        save_volume(VOLUME2_FILE, self.music.get_volume())
                        self.player.reset_movement()
                        return False
                    elif event.button == self.back_button:
                        save_volume(VOLUME2_FILE, self.music.get_volume())
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        save_volume(VOLUME2_FILE, self.music.get_volume())
                        self.close_sound.play()
                        return False
                self.resume_button.mouse_event(event)
                self.back_button.mouse_event(event)
                self.value_slider.mouse_event(event)

            self.resume_button.check_cursor(pygame.mouse.get_pos())
            self.resume_button.draw(self.screen)
            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)
            self.value_slider.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class SettingsMenu:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = main_background
        self.cursor = cursor
        self.value_slider = Slider(WINDOW_WIDTH / 2 - 120, 200, 200, 0, 100,
                                   pygame.mixer.music.get_volume() * 100, 'sound2.png',
                                   pygame.mixer.music)
        self.manual_button = Buttons(WINDOW_WIDTH / 2 - 100, 300, 210, 74, 'button.png', 'Manual',
                                     'button_true.png', 'close2.mp3')
        self.description_button = Buttons(WINDOW_WIDTH / 2 - 100, 400, 210, 74, 'button.png',
                                          'Description',
                                          'button_true.png', 'close2.mp3')
        self.delete_progress_button = Buttons(WINDOW_WIDTH / 2 - 140, 500, 300, 74, 'button.png',
                                              'Delete Progress',
                                              'button_true.png', 'close2.mp3')
        self.back_button = Buttons(WINDOW_WIDTH / 2 - 80, 600, 150, 50, 'back.png', '',
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
                    save_volume(VOLUME_FILE, pygame.mixer.music.get_volume())
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
                        ManualWindow(self.screen, 'les.jpg', self.cursor).run()
                    elif event.button == self.description_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        DescriptionWindow(self.screen, 'les.jpg', self.cursor).run()
                    elif event.button == self.delete_progress_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        DeleteProgressWindow(self.screen, self.cursor, self).run()
                self.value_slider.mouse_event(event)
                self.manual_button.mouse_event(event)
                self.description_button.mouse_event(event)
                self.delete_progress_button.mouse_event(event)
                self.back_button.mouse_event(event)

            self.value_slider.draw(self.screen)
            self.manual_button.check_cursor(pygame.mouse.get_pos())
            self.manual_button.draw(self.screen)
            self.description_button.check_cursor(pygame.mouse.get_pos())
            self.description_button.draw(self.screen)
            self.delete_progress_button.check_cursor(pygame.mouse.get_pos())
            self.delete_progress_button.draw(self.screen)
            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class ManualWindow:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
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
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 95))
            self.screen.blit(text, text_rect)
            instructions = [
                '          Управление:',
                'W - Вперёд',
                'S - Назад',
                'A - Влево',
                'D - Вправо',
                'LShift - Выкинуть',
                'Escape - Назад/Пауза',
                'ЛКМ - Атака',
            ]
            for i, line in enumerate(instructions):
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (WINDOW_WIDTH / 2 - 200, 150 + i * 50))
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


class DescriptionWindow:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
        self.cursor = cursor
        self.back_button = Buttons(WINDOW_WIDTH / 2 - (252 / 2), 600, 252, 74, 'back.png', '',
                                   'back_true.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, 35)
            text = font.render('Описание игры', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 100))
            self.screen.blit(text, text_rect)
            description = [
                'Добро пожаловать в игру "Продержись!"',
                'Ваша цель — выжить в течение 3 минут, избегая ',
                'препятствия на своём пути. Каждый новый уровень ',
                'сложнее предыдущего и открывается только после ',
                'его прохождения! Рискните пройти все 5 уровней!',
                'Удачи!',
                '',
                'Разработчики: Слепов Егор, Пискунов Егор'
            ]
            for i, line in enumerate(description):
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (WINDOW_WIDTH / 2 - 300, 200 + i * 50))
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


class DeleteProgressWindow:
    def __init__(self, screen, cursor, settings_menu):
        self.screen = screen
        self.cursor = cursor
        self.settings_menu = settings_menu
        self.main_background = load_image('les.jpg', '\\main')
        self.back_button = Buttons(WINDOW_WIDTH / 2 - 100, 400, 200, 74, 'button.png', 'Нет',
                                   'button_true.png', 'close2.mp3')
        self.confirm_button = Buttons(WINDOW_WIDTH / 2 - 100, 300, 200, 74, 'button.png', 'Да',
                                      'button_true.png', 'close2.mp3')
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, 35)
            text = font.render('Вы уверены, что хотите удалить сохранённый прогресс?', True,
                               (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 270))
            self.screen.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if event.button == self.back_button:
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        running = False
                    elif event.button == self.confirm_button:
                        pygame.mixer.music.set_volume(0.5)
                        save_volume(VOLUME_FILE, pygame.mixer.music.get_volume())
                        default_volume = 0.5
                        save_volume(VOLUME2_FILE, default_volume)
                        self.settings_menu.value_slider.value = 50
                        default_level_status = [True, False, False, False, False]
                        save_level_status(default_level_status)
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close_sound.play()
                        Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                        return
                self.back_button.mouse_event(event)
                self.confirm_button.mouse_event(event)

            self.back_button.check_cursor(pygame.mouse.get_pos())
            self.back_button.draw(self.screen)
            self.confirm_button.check_cursor(pygame.mouse.get_pos())
            self.confirm_button.draw(self.screen)

            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x - 2, y - 2))
            pygame.display.flip()


class Play:
    def __init__(self, screen, main_background, cursor):
        self.screen = screen
        self.main_background = load_image(main_background, '\\main')
        self.main_background = pygame.transform.scale(self.main_background,
                                                      (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.cursor = cursor
        self.close_sound = pygame.mixer.Sound(load_sounds('close2.mp3'))
        self.buttons = []
        self.back_button = Buttons(
            WINDOW_WIDTH - 170, WINDOW_HEIGHT - 80, 160, 55,
            'back.png', '',
            'back_true.png', 'close2.mp3'
        )
        self.create_buttons()

    def create_buttons(self):
        button_width = 200
        button_height = 80
        total_height = 5 * button_height + 4 * 20
        start_y = (WINDOW_HEIGHT - total_height) // 2
        STATUS_LEVEL = load_level_status()
        for i in range(5):
            x = (WINDOW_WIDTH - button_width) // 2
            y = start_y + i * (button_height + 20)
            if STATUS_LEVEL[4 - i]:
                button = Buttons(
                    x, y,
                    button_width, button_height,
                    'button.png', str(5 - i),
                    'button_true.png', 'close2.mp3'
                )
            else:
                button = Buttons(
                    x, y,
                    button_width, button_height,
                    'button_close.png', str(5 - i),
                    'button_close.png', 'close2.mp3'
                )
            self.buttons.append(button)

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_background, (0, 0))
            font = pygame.font.Font(FONT, FONT_SIZE)
            text = font.render('Выбор уровня', True,
                               (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 40))
            self.screen.blit(text, text_rect)
            difficulty_levels = ['Невозможно', 'Экстремально', 'Сложно', 'Нормально', 'Легко']
            font = pygame.font.Font(FONT, FONT_SIZE)
            for i, button in enumerate(self.buttons):
                difficulty_text = font.render(difficulty_levels[i], True, (255, 255, 255))
                text_rect = difficulty_text.get_rect(
                    center=(button.rect.centerx, button.rect.top - 10))
                self.screen.blit(difficulty_text, text_rect)
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
                    for button in self.buttons:
                        if event.button == button:
                            level_index = self.buttons.index(button)
                            if load_level_status()[4 - level_index]:
                                difficulty = 6 - (5 - level_index)
                                Transition(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT,
                                           MAX_FPS).transition()
                                LevelWindow(self.screen, 'les.jpg', self.cursor,
                                            pygame.mixer.Sound(load_sounds('fight.mp3')),
                                            difficulty).run()
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
                self.screen.blit(cursor, (x - 2, y - 2))
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


def dist_between_objects(x, y, objects, min_distance):
    for el in objects:
        distance = ((x - el.x) ** 2 + (y - el.y) ** 2) ** 0.5
        if distance < min_distance:
            return True
    return False


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


def save_volume(volume_file, volume):
    with open(volume_file, 'w') as file:
        file.write(str(volume))


def load_volume(volume_file):
    try:
        with open(volume_file, 'r') as file:
            return float(file.read())
    except FileNotFoundError:
        return 0.5


def save_level_status(status):
    with open(LEVEL_STATUS, 'w') as file:
        for s in status:
            file.write(f'{int(s)}\n')


def load_level_status():
    try:
        with open(LEVEL_STATUS, 'r') as file:
            return [bool(int(line.strip())) for line in file]
    except FileNotFoundError:
        return [True, False, False, False, False]


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
                save_volume(VOLUME_FILE, pygame.mixer.music.get_volume())
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.button == play_button:
                    Transition(screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    Play(screen, 'les.jpg', cursor).run()
                elif event.button == setting_button:
                    Transition(screen, WINDOW_WIDTH, WINDOW_HEIGHT, MAX_FPS).transition()
                    SettingsMenu(screen, main_background, cursor).run()
                elif event.button == exit_button:
                    save_volume(VOLUME_FILE, pygame.mixer.music.get_volume())
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