import pygame
import os
import sys

FPS = 50

# all_sprites = pygame.sprite.Group()


# Загрузка изображений
def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("bottle.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Кладовщик')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill('white')
    all_sprites.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()
