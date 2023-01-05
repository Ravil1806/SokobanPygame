import pygame
import os
import sys

FPS = 50

player = None

# 3 группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Загрузка изображений
def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('brickwall.png'),
    'empty': load_image('floor.png'),
    'object': load_image('bottle.png'),
    'place': load_image('place.png')
}
player_image = load_image('builder.png')

tile_width = tile_height = 50


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('object', x, y)
            elif level[y][x] == '&':
                Tile('place', x, y)
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Кладовщик')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    mapp = load_level('level1.txt')
    player, level_x, level_y = generate_level(mapp)
    all_sprites.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
    pygame.quit()
