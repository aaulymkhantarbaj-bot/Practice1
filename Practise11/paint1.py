import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

color = (0, 0, 0)
mode = "square"

start_pos = None
drawing = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Режим таңдау
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "square"
            elif event.key == pygame.K_2:
                mode = "right_triangle"
            elif event.key == pygame.K_3:
                mode = "equilateral"
            elif event.key == pygame.K_4:
                mode = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            drawing = False

            x1, y1 = start_pos
            x2, y2 = end_pos

            if mode == "square":
                size = min(abs(x2-x1), abs(y2-y1))
                pygame.draw.rect(screen, color, (x1, y1, size, size), 2)

            elif mode == "right_triangle":
                points = [(x1, y1), (x2, y1), (x1, y2)]
                pygame.draw.polygon(screen, color, points, 2)

            elif mode == "equilateral":
                side = abs(x2 - x1)
                height = side * math.sqrt(3) / 2
                points = [
                    (x1, y1),
                    (x1 + side, y1),
                    (x1 + side/2, y1 - height)
                ]
                pygame.draw.polygon(screen, color, points, 2)

            elif mode == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                points = [
                    (cx, y1),
                    (x2, cy),
                    (cx, y2),
                    (x1, cy)
                ]
                pygame.draw.polygon(screen, color, points, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()