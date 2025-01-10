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
pygame.font.init()
path = pygame.font.match_font("arial")
Font = pygame.font.Font(path, 25)
BONFIREEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BONFIREEVENT, difficult[1] * 1500)
TEMPEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(TEMPEVENT, difficult[1] * 25)


def load_image(name, puth, colorkey=None): ##Загрузка изображений
    fullname = os.path.join(f'files\\world{puth}', name)
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


class Map:
    def __init__(self):
        self.x = 10000
        self.y = 10000

class Player(pygame.sprite.Sprite): ##Класс игрока
    image_w = load_image("forester_w.png", "\\player")
    image_w = pygame.transform.scale(image_w, (60 * pixsel, 60 * pixsel))
    image_e = load_image("forester_e.png", "\\player")
    image_e = pygame.transform.scale(image_e, (60 * pixsel, 60 * pixsel))
    image_s = load_image("forester_s.png", "\\player")
    image_s = pygame.transform.scale(image_s, (60 * pixsel, 60 * pixsel))
    image_n = load_image("forester_n.png", "\\player")
    image_n = pygame.transform.scale(image_n, (60 * pixsel, 60 * pixsel))

    def __init__(self, *group):
        super().__init__(*group)
        global pixsel
        self.image = Player.image_w
        self.rect = self.image.get_rect()
        self.run = [0, 0, 0, 0]
        self.x, self.y = 0, 0
        self.rect.x = width // 2
        self.rect.y = height // 2
        self.count = False
        self.hp = 100
        self.temp = 50

    def update(self, *args):
        global TEMPEVENT
        if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'w':
            self.run[0] = 0
        if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'w':
            self.run[0] = 1
            self.image = Player.image_n
        if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 's':
            self.run[1] = 0
        if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 's':
            self.run[1] = 1
            self.image = Player.image_s
        if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'd':
            self.run[2] = 0
        if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'd':
            self.run[2] = 1
            self.image = Player.image_e
        if args and args[0].type == pygame.KEYUP and pygame.key.name(args[0].key) == 'a':
            self.run[3] = 0
        if args and args[0].type == pygame.KEYDOWN and pygame.key.name(args[0].key) == 'a':
            self.run[3] = 1
            self.image = Player.image_w
        if self.run[0] == 1:
            self.y -= v // FPS
        if self.run[1] == 1:
            self.y += v // FPS
        if self.run[2] == 1:
            self.x += v // FPS
        if self.run[3] == 1:
            self.x -= v // FPS
        if args and args[0].type == TEMPEVENT:
            if (abs(bonfire.rect.x - 320 * pixsel) < 80 * pixsel and
                    abs(bonfire.rect.y - 180 * pixsel) < 80 * pixsel and bonfire.run > 1):
                self.temp = min(self.temp + bonfire.run, 100)
            else:
                if self.temp == 0:
                    self.hp = max(self.hp - 1.25, 0)
                else:
                    self.temp = max(self.temp - 1.25, 0)


class Christmas_Tree(pygame.sprite.Sprite):    ##класс блока - елки
    image = load_image("tree.png", "\\blocks\\tree")
    image2 = load_image("stump.png", "\\blocks\\tree")

    def __init__(self, *group):
        super().__init__(*group)
        global pixsel
        self.image = Christmas_Tree.image
        self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
        self.rect = self.image.get_rect()
        w, h = self.rect.w, self.rect.h
        k = True
        while k:
            x = random.randrange(int(-0.5 * map.x), int(0.5 * map.x))
            y = random.randrange(int(-0.5 * map.y), int(0.5 * map.y))
            if (abs(sorted(all_sprites, key=lambda sprite: sprite.rect.y)[0].rect.y - y) > 100 and
                    abs(sorted(all_sprites, key=lambda sprite: sprite.rect.x)[0].rect.x - x) > 100):
                self.x = x
                self.y = y
                k = False
        self.chopped = False

    def update(self, *args):
        self.rect.x = self.x - player.x + 300 * pixsel
        self.rect.y = self.y - player.y - 200 * pixsel
        if (abs(self.rect.x - 320 * pixsel + 50 * pixsel) < 30 * pixsel and
                abs(self.rect.y - 180 * pixsel + 100 * pixsel) < 30 * pixsel and not self.chopped):
            self.image = Christmas_Tree.image2
            self.image = pygame.transform.scale(self.image, (200 * pixsel, 200 * pixsel))
            player.count = True
            self.chopped = True


class Bonfire(pygame.sprite.Sprite):
    image_0 = load_image("bonfire0.png", "\\blocks\\bonfire")
    image_0 = pygame.transform.scale(image_0, (30 * pixsel, 30 * pixsel))
    image_1 = load_image("bonfire1.png", "\\blocks\\bonfire")
    image_1 = pygame.transform.scale(image_1, (30 * pixsel, 30 * pixsel))
    image_2 = load_image("bonfire2.png", "\\blocks\\bonfire")
    image_2 = pygame.transform.scale(image_2, (30 * pixsel, 30 * pixsel))
    image_3 = load_image("bonfire3.png", "\\blocks\\bonfire")
    image_3 = pygame.transform.scale(image_3, (30 * pixsel, 30 * pixsel))
    image_4 = load_image("bonfire4.png", "\\blocks\\bonfire")
    image_4 = pygame.transform.scale(image_4, (30 * pixsel, 30 * pixsel))
    image_5 = load_image("bonfire5.png", "\\blocks\\bonfire")
    image_5 = pygame.transform.scale(image_5, (30 * pixsel, 30 * pixsel))

    def __init__(self, *group):
        super().__init__(*group)
        global pixsel
        self.image = Bonfire.image_3
        self.rect = self.image.get_rect()
        self.run = 3
        self.x, self.y = 0, 400 * pixsel

    def update(self, *args):
        global BONFIREEVENT, TEMPEVENT
        self.rect.x = self.x - player.x + 300 * pixsel
        self.rect.y = self.y - player.y - 200 * pixsel
        watch = False
        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos) and player.count
                and abs(self.rect.x - 320 * pixsel) < 60 * pixsel and
                abs(self.rect.y - 200 * pixsel) < 60 * pixsel and self.run < 5):
            player.count = False
            self.run = min(self.run + 1, 5)
            watch = True
        if args and args[0].type == BONFIREEVENT:
            self.run = max(self.run - 1, 0)
            watch = True
        if watch:
            if self.run == 0:
                self.image = Bonfire.image_0
            elif self.run == 1:
                self.image = Bonfire.image_1
            elif self.run == 2:
                self.image = Bonfire.image_2
            elif self.run == 3:
                self.image = Bonfire.image_3
            elif self.run == 4:
                self.image = Bonfire.image_4
            elif self.run == 5:
                self.image = Bonfire.image_5
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
    for i in range(difficult[0] * 100):
        Christmas_Tree(all_sprites)
    player = Player(all_sprites)
    print(*all_sprites)
    FPS = 100
    v = 200
    clock = pygame.time.Clock()
    while running:
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
        screen.fill((100, 100, 100))
        clock.tick(FPS)
        sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.rect.y + sprite.rect.h)
        for sprite in sorted_sprites:
            screen.blit(sprite.image, sprite.rect)
        all_sprites.update()
        screen.blit(Font.render(f'x: {player.x} y: {player.y}', 1, (255, 255, 255)), (10, 10))
        screen.blit(Font.render(f'hp: {player.hp}, temp: {player.temp}',
                                1, (255, 255, 255)), (10, 30))
        time += 1
        pygame.display.set_caption(f'survival {time // FPS // 60}:{time//FPS % 60}')
        pygame.display.flip()
    pygame.quit()