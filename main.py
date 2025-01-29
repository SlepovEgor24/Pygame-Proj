import os
import sys
import random
import pygame

difficult = [8, 5]
pygame.init()
pygame.display.set_caption('survival')
size = width, height = 1280, 720
pixsel = height // 360
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
wall = pygame.sprite.Group()
pygame.font.init()
path = pygame.font.match_font("arial")
Font = pygame.font.Font(path, 25)
BONFIREEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BONFIREEVENT, difficult[1] * 15 * 10 * 10 * 2)
TEMPEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(TEMPEVENT, difficult[1] * 25)
MOBEVENT = pygame.USEREVENT + 3
pygame.time.set_timer(MOBEVENT, difficult[1] * 25 * 10 * 10 * 4)


def load_image(name, puth, colorkey=None): ##Загрузка изображений
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
            self.cur_frame = (self.cur_frame + 1) % self.rows + self.run.index(True) * self.columns
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


class Player(pygame.sprite.Sprite): ##Класс игрока
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
        self.rect.x = width // 2
        self.rect.y = height // 2
        self.wood = False
        self.hp = 100
        self.temp = 50

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
            if sprite != self and abs(sprite.x - player.x) < 1280 and abs(sprite.y - player.y) < 720:
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
                else:
                    self.temp = max(self.temp - 1.25, 0)


class ChristmasTree(pygame.sprite.Sprite):    ##класс блока - елки
    image = load_image("tree.png", "\\world\\blocks\\tree")
    image2 = load_image("stump.png", "\\world\\blocks\\tree")

    def __init__(self, *group):
        super().__init__(*group)
        global pixsel
        self.image = ChristmasTree.image
        self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        w, h = self.rect.w, self.rect.h
        while True:
            x = random.randrange(int(-0.7 * map.x), int(0.7 * map.x))
            y = random.randrange(int(-0.7 * map.y), int(0.7 * map.y))
            if x < -200 or x > 100 or y < -100 or y > 400 + self.rect.h:
                self.x = x
                self.y = y
                break
        self.chopped = False

    def update(self, *args):
        self.rect.x = self.x - player.x + 300 * pixsel
        self.rect.y = self.y - player.y - 200 * pixsel
        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos)
            and abs(self.x - player.x) < 300 and abs(self.y - player.y - 500) < 230 and not self.chopped and player.axe):
            self.image = ChristmasTree.image2
            self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
            self.chopped = True
            self.mask = pygame.mask.from_surface(self.image)
            Wood(self.x + self.rect.w // 2, self.y + self.rect.h // 2, all_sprites)


class Wood(pygame.sprite.Sprite):    ##класс блока - елки
    image = load_image("wood.png", "\\world\\blocks\\tree")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        global pixsel
        self.image = Wood.image
        self.image = pygame.transform.scale(self.image, (60 * pixsel, 60 * pixsel))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        w, h = self.rect.w, self.rect.h
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


class Axe(pygame.sprite.Sprite):    ##класс блока - елки
    image = load_image("axe.png", "\\world\\blocks")

    def __init__(self, *group):
        super().__init__(*group)
        global pixsel
        self.image = Axe.image
        self.image = pygame.transform.scale(self.image, (60 * pixsel, 60 * pixsel))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        w, h = self.rect.w, self.rect.h
        while True:
            x = random.randrange(int(-0.05 * map.x), int(0.05 * map.x))
            y = random.randrange(int(-0.05 * map.y), int(0.05 * map.y))
            if abs(x) > 250 and abs(y) > 250:
                self.x = x
                self.y = y
                break

    def update(self, *args):
        self.rect.x = self.x - player.x + 690
        self.rect.y = self.y - player.y + 360
        if pygame.sprite.collide_mask(self, player):
            player.axe = True
            all_sprites.remove(self)
            del self


class Ruins(pygame.sprite.Sprite):
    image2 = load_image("2.png", "\\sprites\\okr1\\2 Objects\\Ruins")
    image3 = load_image("3.png", "\\sprites\\okr1\\2 Objects\\Ruins")
    image4 = load_image("4.png", "\\sprites\\okr1\\2 Objects\\Ruins")
    image5 = load_image("5.png", "\\sprites\\okr1\\2 Objects\\Ruins")

    def __init__(self, *group):
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
        w, h = self.rect.w, self.rect.h
        x = random.randrange(int(-map.x), int(map.x))
        y = random.randrange(int(-map.y), int(map.y))
        self.x = x
        self.y = y

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

    def __init__(self, *group):
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
        w, h = self.rect.w, self.rect.h
        x = random.randrange(int(-map.x), int(map.x))
        y = random.randrange(int(-map.y), int(map.y))
        self.x = x
        self.y = y

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
        self.x, self.y = 0, 400 * pixsel

    def update(self, *args):
        global BONFIREEVENT, TEMPEVENT
        self.rect.x = self.x - player.x + 300 * pixsel
        self.rect.y = self.y - player.y - 200 * pixsel
        watch = False
        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and player.wood
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
        if args and args[0].type == TEMPEVENT and (abs(self.rect.x - 340 * pixsel) < 5 * pixsel and
                abs(self.rect.y - 210 * pixsel) < 5 * pixsel):
            player.hp = max(player.hp - 4 * bonfire.run, 0)
            player.temp = min(player.temp + 4 * bonfire.run, 100)


##Начало работы программы
if __name__ == '__main__':
    running = True
    time = 0
    map = Map()
    bonfire = Bonfire(all_sprites)
    player = Player(all_sprites)
    Axe(all_sprites)
    for i in range(difficult[0] * 100):
        ChristmasTree(all_sprites)
    for i in range(10):
        Ruins(all_sprites)
    for i in range(100):
        Rocks(all_sprites)
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
                    AnimatedSprite(load_image("Boar_Move.png", "\\sprites\\vragi_6\\Monster Pack 21 (Bovine)\\Spritesheets\\Updated Boar"), 6, 4, x, y)
        screen.fill((0, 0, 0))
        clock.tick(FPS)
        wall.draw(screen)
        sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.rect.y + sprite.rect.h)
        for sprite in sorted_sprites:
            if abs(sprite.x - player.x) < 1280 * 2 and abs(sprite.y - player.y) < 720 * 2 + sprite.rect.h:
                screen.blit(sprite.image, sprite.rect)
        all_sprites.update()
        screen.blit(Font.render(f'x: {player.x} y: {player.y}', 1, (255, 255, 255)), (10, 10))
        screen.blit(Font.render(f'hp: {player.hp}, temp: {player.temp}',
                                1, (255, 255, 255)), (10, 30))
        time += 1
        pygame.display.set_caption(f'survival {time // FPS // 60}:{time//FPS % 60}')
        pygame.display.flip()
    pygame.quit()