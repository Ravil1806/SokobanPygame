import os
import sys

import pygame

FPS = 50


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('brickwall.png'),
    'empty': load_image('floor.png')
}
player_image = load_image('worker.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Главное меню", '',
                  'Перемещение героя',
                  'Карта на месте', '',
                  'Нажмите любую кнопку',
                  '     для начала игры']

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 550))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for i in intro_text:
        string_rendered = font.render(i, True, 'black')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '$':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Перемещение героя')
    screen = pygame.display.set_mode((500, 500))
    running = True
    clock = pygame.time.Clock()
    start_screen()
    mapp = load_level('level1.txt')
    player, level_x, level_y = generate_level(mapp)
    all_sprites.draw(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player.rect.x - tile_width > 0 and \
                            mapp[player.y][player.x - 1] != '#':
                        player.x -= 1
                        player.rect.x -= tile_width
                if event.key == pygame.K_UP:
                    if player.rect.y - tile_height > 0 and \
                            mapp[player.y - 1][player.x] != '#':
                        player.y -= 1
                        player.rect.y -= tile_height
                if event.key == pygame.K_DOWN:
                    if player.rect.y + tile_height < 500 and \
                            mapp[player.y + 1][player.x] != '#':
                        player.y += 1
                        player.rect.y += tile_height
                if event.key == pygame.K_RIGHT:
                    if player.rect.x + tile_width < 500 and \
                            mapp[player.y][player.x + 1] != '#':
                        player.x += 1
                        player.rect.x += tile_width
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
