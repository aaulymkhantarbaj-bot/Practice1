import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

snake = [(100, 100)]
direction = "RIGHT"
block = 20

score = 0

# Food генерация
def generate_food():
    return {
        "pos": (random.randrange(0, WIDTH, block),
                random.randrange(0, HEIGHT, block)),
        "value": random.choice([1, 2, 3]),
        "spawn_time": time.time()
    }

food = generate_food()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"

    head_x, head_y = snake[0]

    # Қозғалыс
    if direction == "LEFT":
        head_x -= block
    elif direction == "RIGHT":
        head_x += block
    elif direction == "UP":
        head_y -= block
    elif direction == "DOWN":
        head_y += block

    snake.insert(0, (head_x, head_y))

    # Food жеу
    if snake[0] == food["pos"]:
        score += food["value"]
        food = generate_food()
    else:
        snake.pop()

    # Food timer (5 секунд)
    if time.time() - food["spawn_time"] > 5:
        food = generate_food()

    # Draw snake
    for s in snake:
        pygame.draw.rect(screen, (0, 200, 0), (*s, block, block))

    # Food түсі value-ға байланысты
    if food["value"] == 1:
        color = (255, 0, 0)
    elif food["value"] == 2:
        color = (0, 0, 255)
    else:
        color = (255, 165, 0)

    pygame.draw.rect(screen, color, (*food["pos"], block, block))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()