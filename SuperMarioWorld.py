import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# --- Настройки окна ---
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario World")


def load_image(path):
# --- Загрузка изображений ---
    if not os.path.exists(path):
        print(f"❌ Ошибка: файл '{path}' не найден!")
        pygame.quit()
        sys.exit()
    return pygame.image.load(path)

# Посмотреть верхний блок на наличие проблем работы с выделением файла

try:
    original_image = load_image("assets/SMWSmallMarioSprite.png")
    platform_img = load_image('Semisolid_platform_SMW.png')
    mario_jump = load_image('SMWSmallMarioJumpSprite.png')
    warp_pipe = load_image('Warp_Pipe_SMW.png')
except Exception as e:
    print("Ошибка загрузки:", e)
    sys.exit()

# --- Загрузка звуков ---
try:
    jump_sound = pygame.mixer.Sound('jump_sound.wav')
except pygame.error as e:
    print("⚠️ Не удалось загрузить звук прыжка:", e)
    jump_sound = None

# --- Настройка спрайтов Марио ---
mario_right = original_image
mario_left = pygame.transform.flip(original_image, True, False)
mario_jump_right = mario_jump
mario_jump_left = pygame.transform.flip(mario_jump, True, False)

# --- Позиция и размеры ---
x, y = 100, 100
w, h = original_image.get_width(), original_image.get_height()
facing_right = True

# --- Трубы ---

# --- Платформы ---
platforms = [
    pygame.Rect(0, 360, 65, 1),
    pygame.Rect(60, 360, 65, 1),
    pygame.Rect(120, 360, 65, 1),
    pygame.Rect(180, 360, 65, 1),
    pygame.Rect(240, 360, 65, 1),
    pygame.Rect(300, 360, 65, 1),
]

# --- Физика ---
y_velocity = 0
gravity = 0.8
jump_power = -7
is_on_ground = False
jump_buffer = 0          # Сколько кадров можно "парить"
MAX_JUMP_BUFFER = 15     # Макс. длительность мягкого прыжка

# --- Игровой цикл ---
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Получаем состояние клавиш ---
    keys = pygame.key.get_pressed()

    # --- Горизонтальное движение ---
    speed = 4 if keys[pygame.K_x] else 2
    if keys[pygame.K_LEFT]:
        x -= speed
        facing_right = False
    if keys[pygame.K_RIGHT]:
        x += speed
        facing_right = True

    # --- Запуск прыжка с земли ---
    if keys[pygame.K_z] and is_on_ground:
        y_velocity = jump_power
        is_on_ground = False
        jump_buffer = MAX_JUMP_BUFFER  # Активируем буфер для "мягкого" прыжка
        if jump_sound:
            jump_sound.play()

    # --- Сохраняем предыдущую Y-позицию для коллизии ---
    prev_y = y

    # --- Гравитация + акселерация прыжка ---
    if keys[pygame.K_z] and y_velocity < 0 and jump_buffer > 0:
        # Удержание Z во время подъёма → слабая гравитация → выше прыгаем
        y_velocity += gravity * 0.3
        jump_buffer -= 1
    else:
        # Обычная гравитация
        y_velocity += gravity

    y += y_velocity

    # --- Коллизия с платформами (только сверху) ---
    mario_rect = pygame.Rect(x, y, w, h)
    mario_prev_rect = pygame.Rect(x, prev_y, w, h)
    is_on_ground = False

    for plat in platforms:
        if (y_velocity > 0 and
            mario_prev_rect.bottom <= plat.top and
            mario_rect.bottom >= plat.top and
            mario_rect.left < plat.right and
            mario_rect.right > plat.left):
            y = plat.top - h
            y_velocity = 0
            is_on_ground = True
            jump_buffer = 0  # Сброс буфера при приземлении
            break

    # --- Проверка нижней границы экрана (пол) ---
    if y >= HEIGHT - h:
        y = HEIGHT - h
        y_velocity = 0
        is_on_ground = True
        jump_buffer = 0

    # --- Ограничение по горизонтали ---
    x = max(0, min(x, WIDTH - w))

    # --- Отрисовка ---
    screen.fill((107, 140, 255))  # Голубой фон

    # Платформы
    for plat in platforms:
        screen.blit(platform_img, plat.topleft)
        # pygame.draw.rect(screen, (255, 0, 0), plat, 2)  # отладка (можно раскомментировать)

    # Выбор спрайта: бег или прыжок
    if is_on_ground:
        current_sprite = mario_right if facing_right else mario_left
    else:
        current_sprite = mario_jump_right if facing_right else mario_jump_left

    screen.blit(current_sprite, (x, y))
    # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, w, h), 2)  # отладка

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()