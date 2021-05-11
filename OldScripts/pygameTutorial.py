"""
Python Pokemon Pygame.

Taken from https://coderslegacy.com/python/python-pygame-tutorial/
"""
import pygame
import pygame.locals
import sys
import random
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (29, 159, 74)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 720  # 400
SCREEN_HEIGHT = 336  # 600
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
SPEED = 5
SCORE = 0

# Setting up fonts
font = pygame.font.Font("Pokemon GB.ttf", 60)
font_small = pygame.font.Font("Pokemon GB.ttf", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("background.png")  # 240x112
background = pygame.transform.scale(background, RESOLUTION)

DISPLAYSURF = pygame.display.set_mode(RESOLUTION)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("It's Pokemon bitch!")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("salamence.png")
        self.surf = pygame.Surface((96, 96))
        self.rect = self.surf.get_rect(
            center=(random.randint(48, SCREEN_WIDTH - 48), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(48, SCREEN_WIDTH - 48), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("dragonite.png")
        self.surf = pygame.Surface((96, 96))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 48))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[pygame.locals.K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[pygame.locals.K_DOWN]:
        #     self.rect.move_ip(0,5)
        if self.rect.left > 0:
            if pressed_keys[pygame.locals.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < pygame.display.get_surface().get_width():
            if pressed_keys[pygame.locals.K_RIGHT]:
                self.rect.move_ip(5, 0)


# Setting up sprites
P1 = Player()
E1 = Enemy()

# Creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1500)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and re-draws all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        # pygame.mixer.Sound('sound.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(GREEN)
        DISPLAYSURF.blit(game_over, (100, 100))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
