import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_POWER = -10

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (155, 235, 238)
BLACK = (0, 0, 0)
GREY = (64, 64, 64)

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Параметры птицы
bird_image = pygame.image.load('bird.png')
bird_image = pygame.transform.scale(bird_image, (60, 40))  # Уменьшение изображения
bird_rect = bird_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
velocity = 0

# Параметры труб
pipe_width = 50
pipe_gap = 150
pipe_frequency = 1500
pipe_speed = 5
pipes = []

# Создание новых труб
def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, pipe_frequency)
score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pipe_timer:
            pipes.extend(create_pipe())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = FLAP_POWER

    # Применение гравитации
    velocity += GRAVITY
    bird_rect.y += velocity

    # Движение труб
    pipes = [pipe.move(-pipe_speed, 0) for pipe in pipes]
    pipes = [pipe for pipe in pipes if pipe.right > 0]

    # Проверка прохождения трубы
    for pipe in pipes:
        if pipe.right == bird_rect.left:
            score += 1

    # Проверка столкновений
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            running = False

    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        running = False

    # Отрисовка
    screen.fill(BLUE)
    screen.blit(bird_image, bird_rect)
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Отрисовка счета
    score_text = font.render(f"Score: {score}", True, GREY)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()