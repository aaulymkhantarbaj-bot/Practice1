import pygame, sys
from pygame.locals import *
import random, time, os

pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
MONEY_SCORE = 0
next_speed = 10

# --- PATH FIX ---
BASE_DIR = os.path.dirname(__file__)

def load_image(name):
    return pygame.image.load(os.path.join(BASE_DIR, "image", name))

def load_sound(name):
    return pygame.mixer.Sound(os.path.join(BASE_DIR, "sounds", name))

# Images
moneta = load_image("money.png")
gold_coin = load_image("golden_coin.png")
silver_coin = load_image("silver_coin.png")
bronze_coin = load_image("bronze_coin.png")

background = load_image("AnimatedStreet.png")
icon = load_image("icon.png")

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
pygame.display.set_icon(icon)

# --- CLASSES ---

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.types = [
            {"image": load_image("bronze_coin.png"), "value": 1},
            {"image": load_image("silver_coin.png"), "value": 2},
            {"image": load_image("golden_coin.png"), "value": 3}
        ]

        self.set_random_coin()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def set_random_coin(self):
        current_type = random.choice(self.types)
        self.image = current_type["image"]
        self.value = current_type["value"]

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
            self.set_random_coin()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# Objects
P1 = Player()
E1 = Enemy()
M1 = Coin()

enemies = pygame.sprite.Group(E1)
money = pygame.sprite.Group(M1)

all_sprites = pygame.sprite.Group(P1, E1, M1)

# Sounds
bgsound = load_sound("background.wav")
crash_sound = load_sound("crash.wav")
coin_sound = load_sound("lost_money.wav")

bgsound.play(-1)

# --- GAME LOOP ---
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Speed increase
    if MONEY_SCORE >= next_speed:
        SPEED += 3
        next_speed += 10

    DISPLAYSURF.blit(background, (0, 0))

    # Draw & move
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        bgsound.stop()
        crash_sound.play()
        time.sleep(0.5)

        waiting = True
        while waiting:
            DISPLAYSURF.fill(RED)

            DISPLAYSURF.blit(game_over, (30, 250))

            score = font_small.render(f"Score: {MONEY_SCORE}", True, BLACK)
            DISPLAYSURF.blit(score, (150, 325))

            restart_text = font_small.render("R - restart", True, BLACK)
            quit_text = font_small.render("Q - quit", True, BLACK)

            DISPLAYSURF.blit(restart_text, (150, 500))
            DISPLAYSURF.blit(quit_text, (150, 525))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        waiting = False
                        MONEY_SCORE = 0
                        SPEED = 5

                        E1.rect.top = 0
                        M1.rect.top = 0

                        bgsound.play(-1)

                    if event.key == K_q:
                        pygame.quit()
                        sys.exit()

    # Coin UI
    DISPLAYSURF.blit(bronze_coin, (5, 40))
    DISPLAYSURF.blit(silver_coin, (5, 70))
    DISPLAYSURF.blit(gold_coin, (5, 100))

    DISPLAYSURF.blit(font_small.render("1", True, BLACK), (30, 40))
    DISPLAYSURF.blit(font_small.render("2", True, BLACK), (30, 70))
    DISPLAYSURF.blit(font_small.render("3", True, BLACK), (30, 100))

    # Score
    score_text = font_small.render(str(MONEY_SCORE), True, YELLOW)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Coin collision
    if pygame.sprite.spritecollideany(P1, money):
        coin_sound.play()
        MONEY_SCORE += M1.value
        M1.rect.top = 0
        M1.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        M1.set_random_coin()

    pygame.display.update()
    FramePerSec.tick(FPS)