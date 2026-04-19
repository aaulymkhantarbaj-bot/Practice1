import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# Snake параметрлері
snake_block = 20
snake_speed = 10

snake = [(100, 100)]
direction = "RIGHT"

# Food генерация
def generate_food():
    while True:
        x = random.randrange(0, WIDTH, snake_block)
        y = random.randrange(0, HEIGHT, snake_block)
        if (x, y) not in snake:
            return x, y

food_x, food_y = generate_food()

score = 0
level = 1

font = pygame.font.SysFont(None, 30)

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
        head_x -= snake_block
    elif direction == "RIGHT":
        head_x += snake_block
    elif direction == "UP":
        head_y -= snake_block
    elif direction == "DOWN":
        head_y += snake_block

    # Қабырға collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        print("Game Over")
        running = False

    snake.insert(0, (head_x, head_y))

    # Food жеу
    if head_x == food_x and head_y == food_y:
        score += 1
        food_x, food_y = generate_food()

        # Level өсіру
        if score % 3 == 0:
            level += 1
            snake_speed += 2
    else:
        snake.pop()

    # Snake өзін соқса
    if snake[0] in snake[1:]:
        print("Game Over")
        running = False

    # Салу
    for block in snake:
        pygame.draw.rect(screen, (0, 200, 0), (*block, snake_block, snake_block))

    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, snake_block, snake_block))

    # Score + Level
    text = font.render(f"Score: {score}  Level: {level}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(snake_speed)

pygame.quit()