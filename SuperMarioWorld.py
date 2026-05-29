import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# --- Настройки окна ---
WIDTH, HEIGHT = 512, 432
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario World")

def load_image(path):
    if not os.path.exists(path):
        print(f"❌ Ошибка: файл '{path}' не найден!")
        pygame.quit()
        sys.exit()
    img = pygame.image.load(path)
    return img.convert_alpha()

try:
    original_image = load_image("./assets/SMWSmallMarioSprite.png")
    mario_jump = load_image('./assets/SMWSmallMarioJumpSprite.png')
    warp_pipe = load_image('./assets/Warp_Pipe_SMW.png')
    tile_img = load_image('./assets/tile1.png')
    box_img = load_image('./assets/box.png')
    def_block = load_image('./assets/SMW_RotatingBlock.png')
    mario_fall = load_image('./assets/fall.png')
    mario_up = load_image('./assets/up.png')
    mario_down = load_image('./assets/down.png')
    mini_pip = load_image('./assets/mini_pipe.png')
    
    try:
        mario_walk_frames_right = [
            load_image('./assets/marioWalk1.png'),
            load_image('./assets/marioWalk2.png'),
        ]
    except Exception:
        mario_walk_frames_right = [original_image] * 2
        
    mario_walk_frames_left = [pygame.transform.flip(img, True, False) for img in mario_walk_frames_right]
    
    goomba_frames_right = [load_image('./assets/goomba1.png'), load_image('./assets/goomba2.png')]
    goomba_frames_left = [pygame.transform.flip(img, True, False) for img in goomba_frames_right]
    
except Exception as e:
    print("Ошибка загрузки:", e)
    sys.exit()

background_img = None
try:
    background_img = load_image('./assets/background.png')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
except Exception:
    pass

try:
    jump_sound = pygame.mixer.Sound('jump_sound.wav')
except pygame.error as e:
    print("⚠️ Не удалось загрузить звук прыжка:", e)
    jump_sound = None

try:
    pygame.mixer.music.load('overworld.wav')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.4)
except pygame.error as e:
    print("⚠️ Не удалось загрузить фоновую музыку:", e)

# --- Спрайты Марио (статичные) ---
mario_right = original_image
mario_left = pygame.transform.flip(original_image, True, False)
mario_jump_right = mario_jump
mario_jump_left = pygame.transform.flip(mario_jump, True, False)
mario_fall_right = mario_fall
mario_fall_left = pygame.transform.flip(mario_fall, True, False)
mario_up_right = mario_up
mario_up_left = pygame.transform.flip(mario_up, True, False)
mario_down_right = mario_down
mario_down_left = pygame.transform.flip(mario_down, True, False)

x, y = 100, 384
w, h = original_image.get_width(), original_image.get_height()
facing_right = True

mario_anim_idx = 0          
mario_anim_timer = 0        
MARIO_WALK_SPEED = 6        

pipe_rect = warp_pipe.get_rect(topleft=(400, 384))
pipe_mini = mini_pip.get_rect(topleft=(160, 400))

blocks = [
    def_block.get_rect(topleft=(112, 336)),
    def_block.get_rect(topleft=(128, 336)),
    def_block.get_rect(topleft=(144, 336)),
    def_block.get_rect(topleft=(160, 336)),
    def_block.get_rect(topleft=(176, 336))
]

box_rect = box_img.get_rect(topleft=(0, 384))

tile_size = 16
tile_size_r = 208
tile_rects = [pygame.Rect(tx, HEIGHT - tile_size, tile_size, tile_size) for tx in range(0, WIDTH, tile_size)]
tile_surface = pygame.transform.scale(tile_img, (tile_size_r, tile_size))

solids = tile_rects + [pipe_rect] + blocks + [pipe_mini]

y_velocity = 0
gravity = 0.6
jump_power = -6
is_on_ground = False
jump_buffer = 0
MAX_JUMP_BUFFER = 8

# --- ГОМБА (Goomba) ---
goomba_w, goomba_h = goomba_frames_right[0].get_width(), goomba_frames_right[0].get_height()
goomba_x, goomba_y = 350, 400
goomba_dx = -1.2
goomba_dy = 0.0
goomba_alive = True
goomba_gravity = 0.6
goomba_rect = pygame.Rect(goomba_x, goomba_y, goomba_w, goomba_h)

goomba_anim_idx = 0
goomba_anim_timer = 0
GOOMBA_ANIM_SPEED = 10

# === ТАЙМЕР РЕСПАВНА ГУМБЫ ===
goomba_death_time = 0
GOOMBA_RESPAWN_DELAY = 5000
goomba_spawning = False
goomba_spawn_timer = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ==================== ГОРИЗОНТАЛЬНОЕ ДВИЖЕНИЕ МАРИО ====================
    speed = 4 if keys[pygame.K_x] else 3
    dx = 0
    if keys[pygame.K_LEFT]:
        dx -= speed
        facing_right = False
    if keys[pygame.K_RIGHT]:
        dx += speed
        facing_right = True

    is_moving = (dx != 0) and is_on_ground
    
    if is_moving:
        mario_anim_timer += 1
        if mario_anim_timer >= MARIO_WALK_SPEED:
            mario_anim_idx = (mario_anim_idx + 1) % len(mario_walk_frames_right)
            mario_anim_timer = 0
    else:
        mario_anim_idx = 0
        mario_anim_timer = 0

    x += dx
    mario_rect = pygame.Rect(x, y, w, h)
    for solid in solids:
        if mario_rect.colliderect(solid):
            if dx > 0:
                x = solid.left - w
            elif dx < 0:
                x = solid.right
            mario_rect.x = x

    # ==================== ВЕРТИКАЛЬНОЕ ДВИЖЕНИЕ МАРИО ====================
    if keys[pygame.K_z] and is_on_ground:
        y_velocity = jump_power
        is_on_ground = False
        jump_buffer = MAX_JUMP_BUFFER
        if jump_sound:
            jump_sound.play()

    if keys[pygame.K_z] and y_velocity < 0 and jump_buffer > 0:
        y_velocity += gravity * 0.1
        jump_buffer -= 1
    else:
        y_velocity += gravity

    prev_y = y
    y += y_velocity
    mario_rect.y = y
    prev_mario_rect = pygame.Rect(x, prev_y, w, h)

    for solid in solids:
        if mario_rect.colliderect(solid):
            if y_velocity > 0:
                y = solid.top - h
                y_velocity = 0
                is_on_ground = True
                jump_buffer = 0
            elif y_velocity < 0:
                y = solid.bottom
                y_velocity = 0
            mario_rect.y = y

    if mario_rect.colliderect(box_rect):
        if y_velocity > 0 and prev_mario_rect.bottom <= box_rect.top:
            y = box_rect.top - h
            y_velocity = 0
            is_on_ground = True
            jump_buffer = 0
            mario_rect.y = y

    x = max(0, min(x, WIDTH - w))
    if y > HEIGHT:
        y = 0
        y_velocity = 0

    # ==================== ЛОГИКА ГУМБЫ ====================
    if goomba_alive:
        goomba_anim_timer += 1
        if goomba_anim_timer >= GOOMBA_ANIM_SPEED:
            goomba_anim_idx = (goomba_anim_idx + 1) % len(goomba_frames_right)
            goomba_anim_timer = 0

        if goomba_spawning:
            # 🔧 Фаза появления: гравитация ОТКЛЮЧЕНА, спрайт плавно поднимается
            goomba_spawn_timer += 1
            target_y = pipe_rect.top - goomba_h  # Финальная позиция на верху трубы
            
            if goomba_y > target_y:
                goomba_y -= 2.5  # Скорость подъёма
            else:
                goomba_y = target_y
            goomba_rect.y = goomba_y

            # Завершаем анимацию через ~0.5 сек
            if goomba_spawn_timer >= 30:
                goomba_spawning = False
                goomba_dy = 0
                goomba_rect.y = goomba_y
        else:
            # Обычное движение
            goomba_x += goomba_dx
            goomba_rect.x = goomba_x
            for solid in solids:
                if goomba_rect.colliderect(solid):
                    if goomba_dx > 0:
                        goomba_x = solid.left - goomba_w
                        goomba_dx = -goomba_dx
                    elif goomba_dx < 0:
                        goomba_x = solid.right
                        goomba_dx = -goomba_dx
                    goomba_rect.x = goomba_x

            goomba_dy += goomba_gravity
            goomba_y += goomba_dy
            goomba_rect.y = goomba_y
            for solid in solids:
                if goomba_rect.colliderect(solid):
                    if goomba_dy > 0:
                        goomba_y = solid.top - goomba_h
                        goomba_dy = 0
                    elif goomba_dy < 0:
                        goomba_y = solid.bottom
                        goomba_dy = 0
                    goomba_rect.y = goomba_y

            if goomba_x <= 0:
                goomba_x = 0
                goomba_dx = abs(goomba_dx)
            elif goomba_x + goomba_w >= WIDTH:
                goomba_x = WIDTH - goomba_w
                goomba_dx = -abs(goomba_dx)

            if goomba_y > HEIGHT + 50:
                goomba_x, goomba_y = 350, 0
                goomba_dx = -1.2
                goomba_dy = 0
                goomba_rect.topleft = (goomba_x, goomba_y)

        # Коллизия с Марио (игнорируется, пока Гумба выходит из трубы)
        mario_rect_now = pygame.Rect(x, y, w, h)
        if mario_rect_now.colliderect(goomba_rect) and not goomba_spawning:
            prev_mario_bottom = (y - y_velocity) + h
            if y_velocity > 0 and prev_mario_bottom <= goomba_rect.top + 12:
                goomba_alive = False
                goomba_death_time = pygame.time.get_ticks()
                y_velocity = -5
                if jump_sound:
                    jump_sound.play()
            else:
                x, y = 100, 384
                y_velocity = 0
                facing_right = True
                print("💀 Марио коснулся Гумбы!")

    # ==================== РЕСПАВН ГУМБЫ ====================
    if not goomba_alive:
        if pygame.time.get_ticks() - goomba_death_time >= GOOMBA_RESPAWN_DELAY:
            goomba_alive = True
            goomba_spawning = True
            goomba_spawn_timer = 0
            goomba_x = pipe_rect.centerx - goomba_w // 2
            goomba_y = pipe_rect.top + 5  
            goomba_dx = -1.2
            goomba_dy = 0
            goomba_rect.topleft = (goomba_x, goomba_y)
            goomba_anim_idx = 0
            goomba_anim_timer = 0

    # ==================== ОТРИСОВКА ====================
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((107, 140, 255))

    for t_rect in tile_rects:
        screen.blit(tile_surface, t_rect.topleft)

    screen.blit(box_img, box_rect.topleft)
    for b in blocks:
        screen.blit(def_block, b.topleft)
    screen.blit(warp_pipe, pipe_rect.topleft)
    screen.blit(mini_pip, pipe_mini.topleft)

    if goomba_alive:
        frames = goomba_frames_right if goomba_dx > 0 else goomba_frames_left
        screen.blit(frames[goomba_anim_idx], (goomba_x, goomba_y))

    if not is_on_ground:
        if y_velocity < 0:
            current_sprite = mario_jump_right if facing_right else mario_jump_left
        else:
            current_sprite = mario_fall_right if facing_right else mario_fall_left
    else:
        if is_moving:
            frames = mario_walk_frames_right if facing_right else mario_walk_frames_left
            current_sprite = frames[mario_anim_idx]
        elif keys[pygame.K_UP]:
            current_sprite = mario_up_right if facing_right else mario_up_left
        elif keys[pygame.K_DOWN]:
            current_sprite = mario_down_right if facing_right else mario_down_left
        else:
            current_sprite = mario_right if facing_right else mario_left

    screen.blit(current_sprite, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()