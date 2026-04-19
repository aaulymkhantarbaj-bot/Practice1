import pygame
import random

pygame.init()

# Экран
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# Түстер
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Машина
car_width = 50
car_height = 100
car_x = WIDTH // 2
car_y = HEIGHT - 120
car_speed = 5

# Coin
coin_size = 20
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = -50
coin_speed = 4
coins_collected = 0

# Шрифт
font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Батырмалар
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    # Coin қозғалысы
    coin_y += coin_speed
    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(0, WIDTH - coin_size)

    # Collision (машина мен coin)
    if (car_x < coin_x < car_x + car_width and
        car_y < coin_y < car_y + car_height):
        coins_collected += 1
        coin_y = -50
        coin_x = random.randint(0, WIDTH - coin_size)

    # Машина салу
    pygame.draw.rect(screen, BLACK, (car_x, car_y, car_width, car_height))

    # Coin салу
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_size)

    # Coin саны
    text = font.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()