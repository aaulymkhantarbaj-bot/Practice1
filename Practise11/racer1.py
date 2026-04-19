import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player = pygame.Rect(180, 500, 40, 80)
player_speed = 5

# Enemy
enemy = pygame.Rect(random.randint(0, 360), 0, 40, 80)
enemy_speed = 5

# Coins (әр coin-ның value болады)
coins = []
coin_spawn_timer = 0

score = 0

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player қозғалысы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Enemy қозғалысы
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(0, 360)

    # Coin генерация (рандом)
    coin_spawn_timer += 1
    if coin_spawn_timer > 50:
        coin_spawn_timer = 0

        # weight = coin value (1, 2, 3)
        value = random.choice([1, 2, 3])
        coin = {
            "rect": pygame.Rect(random.randint(0, 380), 0, 20, 20),
            "value": value,
            "speed": 3
        }
        coins.append(coin)

    # Coins қозғалысы
    for coin in coins:
        coin["rect"].y += coin["speed"]

        # Collision (player coin)
        if player.colliderect(coin["rect"]):
            score += coin["value"]
            coins.remove(coin)

    # Enemy speed increase
    if score >= 10:
        enemy_speed = 8
    if score >= 20:
        enemy_speed = 12

    # Drawing
    pygame.draw.rect(screen, BLACK, player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)

    # Coins draw (value бойынша түс өзгереді)
    for coin in coins:
        if coin["value"] == 1:
            color = (255, 215, 0)
        elif coin["value"] == 2:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        pygame.draw.circle(screen, color, coin["rect"].center, 10)

    # Score
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()