import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

drawing = False
mode = "draw"  # draw, rect, circle, erase
color = (0, 0, 0)

start_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Перне арқылы режим ауыстыру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "erase"
            elif event.key == pygame.K_d:
                mode = "draw"

            # Түстер
            elif event.key == pygame.K_1:
                color = (255, 0, 0)
            elif event.key == pygame.K_2:
                color = (0, 255, 0)
            elif event.key == pygame.K_3:
                color = (0, 0, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                pygame.draw.rect(screen, color, (*start_pos, end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]), 2)

            elif mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 2)

    if drawing and mode == "draw":
        pygame.draw.circle(screen, color, pygame.mouse.get_pos(), 3)

    if drawing and mode == "erase":
        pygame.draw.circle(screen, (255, 255, 255), pygame.mouse.get_pos(), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()