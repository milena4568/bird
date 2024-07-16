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
GREEN = (0, 220, 0)
RED = (240, 0, 45)
BLUE = (155, 235, 238)
BLACK = (0, 0, 0)
GREY = (64, 64, 64)
ORANGE = (255, 140, 105)
LIGHT_BLUE = (173, 216, 230)

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Параметры птицы
bird_images = [pygame.image.load('bird3.png'), pygame.image.load('bird4.png'), pygame.image.load('bird3.png')]
bird_images = [pygame.transform.scale(img, (60, 40)) for img in bird_images]  # Уменьшение изображений
bird_index = 0  # Индекс текущего изображения птицы
bird_rect = bird_images[bird_index].get_rect(center=(WIDTH // 4, HEIGHT // 2))
velocity = 0
bird_died_image = pygame.image.load('bird5.png')
bird_died_image = pygame.transform.scale(bird_died_image, (60, 40))

# Параметры труб
pipe_width = 50
pipe_gap = 150
pipe_frequency = 1500
pipe_speed = 5
pipes = []

# Фон
background_image = pygame.image.load('fon.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Кнопки
start_button_image = pygame.image.load('start_button.png')
start_button_image = pygame.transform.scale(start_button_image, (100, 50))
exit_button_image = pygame.image.load('exit_button.png')
exit_button_image = pygame.transform.scale(exit_button_image, (100, 50))
retry_button_image = pygame.image.load('retry_button.png')
retry_button_image = pygame.transform.scale(retry_button_image, (100, 50))

# Текстовые изображения
flappy_bird_image = pygame.image.load('flappy_bird.png')
flappy_bird_image = pygame.transform.scale(flappy_bird_image, (200, 50))
game_over_image = pygame.image.load('game_over.png')
game_over_image = pygame.transform.scale(game_over_image, (200, 50))

# Загрузка шрифта EpilepsySans
pygame.font.init()
font = pygame.font.Font('EpilepsySans.ttf', 36)

# Загрузка музыки
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Настройка громкости музыки
pygame.mixer.music.play(-1)  # -1 для зацикливания музыки

# Создание новых труб
def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

# Функция для отображения экрана проигрыша
def show_game_over_screen():
    screen.fill(RED)  # Изменен цвет фона на красный
    screen.blit(game_over_image, (WIDTH // 2 - game_over_image.get_width() // 2, HEIGHT // 2 - 100))

    retry_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 50)

    screen.blit(retry_button_image, retry_button.topleft)
    screen.blit(exit_button_image, exit_button.topleft)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if retry_button.collidepoint(mouse_pos):
                    return True
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

# Функция для отображения стартового экрана
def show_start_screen():
    screen.blit(background_image, (0, 0))
    screen.blit(flappy_bird_image, (WIDTH // 2 - flappy_bird_image.get_width() // 2, HEIGHT // 2 - 100))

    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 70, 100, 50)

    screen.blit(start_button_image, start_button.topleft)
    screen.blit(exit_button_image, exit_button.topleft)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()

# Функция для отображения кнопки звука
def draw_sound_button(sound_on):
    sound_button_image = pygame.image.load('sound_on.png') if sound_on else pygame.image.load('sound_off.png')
    sound_button_image = pygame.transform.scale(sound_button_image, (50, 50))
    screen.blit(sound_button_image, (WIDTH - 70, 10))

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, pipe_frequency)
score = 0
sound_on = True
pause_start_time = 0

show_start_screen()  # Показываем стартовый экран перед началом игры

while running:
    game_over = False
    bird_rect.center = (WIDTH // 4, HEIGHT // 2)
    velocity = 0
    pipes = []
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pipe_timer:
                pipes.append(create_pipe())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = FLAP_POWER
                    bird_index = (bird_index + 1) % len(bird_images)  # Переключение между изображениями птицы
                elif event.key == pygame.K_m:
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if WIDTH - 70 <= event.pos[0] <= WIDTH - 20 and 10 <= event.pos[1] <= 60:
                        sound_on = not sound_on
                        if sound_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

        # Применение гравитации
        velocity += GRAVITY
        bird_rect.y += velocity

        # Движение труб
        pipes = [(pipe_top.move(-pipe_speed, 0), pipe_bottom.move(-pipe_speed, 0)) for pipe_top, pipe_bottom in pipes]
        pipes = [pair for pair in pipes if pair[0].right > 0]

        # Проверка прохождения трубы
        for pipe_top, pipe_bottom in pipes:
            if pipe_top.right == bird_rect.left:
                score += 1

        # Проверка столкновений
        for pipe_top, pipe_bottom in pipes:
            if bird_rect.colliderect(pipe_top) or bird_rect.colliderect(pipe_bottom):
                game_over = True

        if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
            game_over = True

        # Отрисовка
        screen.blit(background_image, (0, 0))
        if game_over:
            screen.blit(bird_died_image, bird_rect)  # Отображаем птицу после смерти
            if pause_start_time == 0:
                pause_start_time = pygame.time.get_ticks()  # Запоминаем время начала паузы
            elif pygame.time.get_ticks() - pause_start_time >= 5000:  # Пауза 5 секунд
                game_over = True
        else:
            screen.blit(bird_images[bird_index], bird_rect)  # Отображаем обычную птицу
        for pipe_top, pipe_bottom in pipes:
            pygame.draw.rect(screen, GREEN, pipe_top)
            pygame.draw.rect(screen, GREEN, pipe_bottom)

        # Отрисовка счета
        score_text = font.render(f"Score: {score}", True, BLACK)  # Использование шрифта EpilepsySans и черного цвета
        screen.blit(score_text, (10, 10))

        # Рисуем кнопку звука
        draw_sound_button(sound_on)

        pygame.display.flip()
        clock.tick(30)

    # Показать экран проигрыша
    if show_game_over_screen():
        continue
    else:
        break

pygame.quit()