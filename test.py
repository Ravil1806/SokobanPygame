from time import sleep
import pygame_widgets
from pygame_widgets.button import Button
import pygame
import os
import sys

FPS = 30

player = None
moves = 0
places = {}
clock = pygame.time.Clock()
tile_width = tile_height = 50

# 3 группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bottles_group = pygame.sprite.Group()


# Загрузка изображений
def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


# Изображения
tile_images = {
    'wall': load_image('brickwall.png'),
    'empty': load_image('floor.png'),
    'place': load_image('place.png')
}
player_image = load_image('worker.png')
bottle_image = load_image('bottle.png')


# Загрузка уровней
def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# Клетка
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * self.x, tile_height * self.y)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(
            tile_width * self.x, tile_height * self.y)


# Бутылка
class Bottle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bottles_group, all_sprites)
        self.image = bottle_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * self.x, tile_height * self.y)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(
            tile_width * self.x, tile_height * self.y)

    def update(self, x, y):
        self.move(x, y)
        if cur_level[y][x] == '&':
            places[f'{x} {y}'] = 1

# Заставка игры
# def start_screen():
#     intro_text = ['Нажмите на любую кнопку',
#                   '          для начала игры']
#
#     fon = pygame.transform.scale(load_image('fon.jpg'), (1000, 750))
#     screen.blit(fon, (0, 0))
#     font = pygame.font.Font(None, 50)
#     text_coord = 200
#     for i in intro_text:
#         string_rendered = font.render(i, True, 'yellow')
#         intro_rect = string_rendered.get_rect()
#         text_coord += 10
#         intro_rect.top = text_coord
#         intro_rect.x = 120
#         text_coord += intro_rect.height
#         screen.blit(string_rendered, intro_rect)
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 terminate()
#             elif event.type == pygame.KEYDOWN or \
#                     event.type == pygame.MOUSEBUTTONDOWN:
#                 return
#         pygame.display.flip()
#         clock.tick(FPS)


# Генерация уровня
def generate_level(lvl):
    new_player, x, y = None, None, None
    for y in range(len(lvl)):
        for x in range(len(lvl[y])):
            if lvl[y][x] == '.':
                Tile('empty', x, y)
            elif lvl[y][x] == '#':
                Tile('wall', x, y)
            elif lvl[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif lvl[y][x] == '$':
                Tile('empty', x, y)
                Bottle(x, y)
            elif lvl[y][x] == '&':
                places[f'{x} {y}'] = 0
                Tile('place', x, y)
    return new_player, x, y


def end_of_the_game():
    pass


# Основной цикл игры
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Кладовщик')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    # start_screen()
    font = pygame.font.Font(None, 50)
    level = 0
    levels = [load_level('test.txt'),
              load_level('test2.txt'),
              load_level('test3.txt')]
    cur_level = levels[level]
    player, level_x, level_y = generate_level(cur_level)
    all_sprites.draw(screen)

    moveLeft, moveRight, moveUp, moveDown = False, False, False, False

    running = True
    moving = False
    end = False

    def next_level():
        global end, level, cur_level, moves, \
            player, level_x, level_y, all_sprites
        button.hide()
        end = False
        level += 1
        cur_level = levels[level]
        moves = 0
        for i in all_sprites:
            i.kill()
        player, level_x, level_y = generate_level(cur_level)
        all_sprites.draw(screen)

    button = Button(
        screen,
        840,
        5,
        150,
        40,
        text='След. уровень',
        fontSize=30,
        inactiveColour='yellow',
        hoverColour='yellow',
        pressedColour='green',
        onClick=next_level
    )
    button.hide()

    while running:
        events = pygame.event.get()
        for event in events:

            if end:
                button.show()

            if event.type == pygame.QUIT:
                terminate()

            # Управление
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == pygame.K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == pygame.K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == pygame.K_DOWN:
                    moveUp = False
                    moveDown = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moveLeft = False
                if event.key == pygame.K_RIGHT:
                    moveRight = False
                if event.key == pygame.K_UP:
                    moveUp = False
                if event.key == pygame.K_DOWN:
                    moveDown = False

        if moveLeft:
            if cur_level[player.y][player.x - 1] != '#' and \
                    cur_level[player.y][player.x - 2] != '#':
                player.move(player.x - 2, player.y)
                if pygame.sprite.spritecollideany(player, bottles_group):
                    player.move(player.x + 1, player.y)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        player.move(player.x + 1, player.y)
                    else:
                        moves += 1
                else:
                    player.move(player.x + 2, player.y)
                    moving = True
            else:
                moving = True
            if moving:
                if cur_level[player.y][player.x - 1] != '#':
                    player.move(player.x - 1, player.y)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        if cur_level[player.y][player.x - 1] != '#':
                            pygame.sprite.spritecollideany(player,
                                bottles_group).update(player.x - 1, player.y)
                            if cur_level[player.y][player.x - 1] == '&':
                                places[f'{player.x - 1} {player.y}'] = 1
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                                    places[f'{player.x - 1} {player.y}'] = 1
                            else:
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                            moves += 1
                        else:
                            player.move(player.x + 1, player.y)
                    else:
                        moves += 1
            sleep(0.15)
            moving = False
        if moveRight:
            if cur_level[player.y][player.x + 1] != '#' and \
                    cur_level[player.y][player.x + 2] != '#':
                player.move(player.x + 2, player.y)
                if pygame.sprite.spritecollideany(player, bottles_group):
                    player.move(player.x - 1, player.y)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        player.move(player.x - 1, player.y)
                    else:
                        moves += 1
                else:
                    player.move(player.x - 2, player.y)
                    moving = True
            else:
                moving = True
            if moving:
                if cur_level[player.y][player.x + 1] != '#':
                    player.move(player.x + 1, player.y)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        if cur_level[player.y][player.x + 1] != '#':
                            pygame.sprite.spritecollideany(player,
                                bottles_group).update(player.x + 1, player.y)
                            if cur_level[player.y][player.x + 1] == '&':
                                places[f'{player.x + 1} {player.y}'] = 1
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                                    places[f'{player.x + 1} {player.y}'] = 1
                            else:
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                            moves += 1
                        else:
                            player.move(player.x - 1, player.y)
                    else:
                        moves += 1
            sleep(0.15)
            moving = False
        if moveUp:
            if cur_level[player.y - 1][player.x] != '#' and \
                    cur_level[player.y - 2][player.x] != '#':
                player.move(player.x, player.y - 2)
                if pygame.sprite.spritecollideany(player, bottles_group):
                    player.move(player.x, player.y + 1)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        player.move(player.x, player.y + 1)
                    else:
                        moves += 1
                else:
                    player.move(player.x, player.y + 2)
                    moving = True
            else:
                moving = True
            if moving:
                if cur_level[player.y - 1][player.x] != '#':
                    player.move(player.x, player.y - 1)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        if cur_level[player.y - 1][player.x] != '#':
                            pygame.sprite.spritecollideany(player,
                                bottles_group).update(player.x, player.y - 1)
                            if cur_level[player.y - 1][player.x] == '&':
                                places[f'{player.x} {player.y - 1}'] = 1
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                                    places[f'{player.x } {player.y - 1}'] = 1
                            else:
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                            moves += 1
                        else:
                            player.move(player.x, player.y + 1)
                    else:
                        moves += 1
            sleep(0.15)
            moving = False
        if moveDown:
            if cur_level[player.y + 1][player.x] != '#' and \
                    cur_level[player.y + 2][player.x] != '#':
                player.move(player.x, player.y + 2)
                if pygame.sprite.spritecollideany(player, bottles_group):
                    player.move(player.x, player.y - 1)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        player.move(player.x, player.y - 1)
                    else:
                        moves += 1
                else:
                    player.move(player.x, player.y - 2)
                    moving = True
            else:
                moving = True
            if moving:
                if cur_level[player.y + 1][player.x] != '#':
                    player.move(player.x, player.y + 1)
                    if pygame.sprite.spritecollideany(player, bottles_group):
                        if cur_level[player.y + 1][player.x] != '#':
                            pygame.sprite.spritecollideany(player,
                                bottles_group).update(player.x, player.y + 1)
                            if cur_level[player.y + 1][player.x] == '&':
                                places[f'{player.x} {player.y + 1}'] = 1
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                                    places[f'{player.x } {player.y + 1}'] = 1
                            else:
                                if cur_level[player.y][player.x] == '&':
                                    places[f'{player.x} {player.y}'] = 0
                            moves += 1
                        else:
                            player.move(player.x, player.y - 1)
                    else:
                        moves += 1
            sleep(0.15)
            moving = False

        clock.tick(FPS)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        bottles_group.draw(screen)
        player_group.draw(screen)
        screen.blit(font.render(f'Шагов: {moves}', True, 'black'), (10, 10))

        if all(places.values()):
            if level < len(levels) - 1:
                end = True
            else:
                screen.blit(font.render(f'Вы прошли все уровни!', True,
                                        'white'), (300, 300))
                for i in all_sprites:
                    i.kill()

        pygame_widgets.update(events)
        pygame.display.flip()
    pygame.quit()
