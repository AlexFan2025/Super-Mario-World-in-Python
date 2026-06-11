import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# --- Настройки окна ---
WIDTH, HEIGHT = 512, 432
score = 0
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score_text = font.render(f"Enemie count: {score}", True, WHITE)
pygame.display.set_caption("Super Mario World")

def load_image(path):
    if not os.path.exists(path):
        print(f"❌ Ошибка: файл '{path}' не найден!")
        return pygame.Surface((16, 16), pygame.SRCALPHA)
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
    mario_death_raw = load_image('./assets/Mario_SMW_dying_sprite.png')
    ice_block = load_image('./assets/IceBlock.png')
    
    # --- ИСПРАВЛЕНИЕ: Масштабируем блок до размера тайла 16x16 ---
    def_block_scaled = pygame.transform.scale(def_block, (16, 16))
    
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

    goombrat_frames_right = [load_image('./assets/Goombrat1.png'), load_image('./assets/Goombrat2.png')]
    goombrat_frames_left = [pygame.transform.flip(img, True, False) for img in goombrat_frames_right]
    
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
    death_sound = pygame.mixer.Sound('PlayerDown.mp3')
except pygame.error as e:
    print("⚠️ Не удалось загрузить звуки:", e)
    jump_sound = None
    death_sound = None

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
mario_death = mario_death_raw

# --- Начальные позиции для сброса уровня ---
START_X, START_Y = 100, 384
x, y = START_X, START_Y
w, h = original_image.get_width(), original_image.get_height()
facing_right = True

# --- НОВОЕ: Переменная для инерции (текущая горизонтальная скорость) ---
mario_dx = 0.0

mario_anim_idx = 0          
mario_anim_timer = 0        
MARIO_WALK_SPEED = 6        

pipe_rect = warp_pipe.get_rect(topleft=(400, 384))
pipe_mini = mini_pip.get_rect(topleft=(160, 400))

def_blocks = [pygame.Rect(112, 336, 96, 16)]

box_rect = box_img.get_rect(topleft=(0, 384))

tile_size = 16
tile_size_r = 208
tile_rects = [pygame.Rect(tx, HEIGHT - tile_size, tile_size, tile_size) for tx in range(0, WIDTH, tile_size)]
tile_surface = pygame.transform.scale(tile_img, (tile_size_r, tile_size))

# --- Ледяные блоки ---
ice_blocks = [pygame.Rect(208, 336, 64, 16)] # x, y, ширина, высота
solids = tile_rects + [pipe_rect] + def_blocks + [pipe_mini] + ice_blocks

# Масштабируем ледяной блок для отрисовки (предполагаем, что тайл 16x16)
ice_block_scaled = pygame.transform.scale(ice_block, (16, 16))

y_velocity = 0
gravity = 0.6
jump_power = -6
is_on_ground = False
jump_buffer = 0
MAX_JUMP_BUFFER = 8

# --- ГОМБА (Goomba) ---
goomba_w, goomba_h = goomba_frames_right[0].get_width(), goomba_frames_right[0].get_height()
GOOMBA_START_X, GOOMBA_START_Y = 350, 400
goomba_x, goomba_y = GOOMBA_START_X, GOOMBA_START_Y
goomba_dx = -1.2
goomba_dy = 0.0
goomba_alive = True
goomba_gravity = 0.6
goomba_rect = pygame.Rect(goomba_x, goomba_y, goomba_w, goomba_h)

goomba_anim_idx = 0
goomba_anim_timer = 0
GOOMBA_ANIM_SPEED = 10

goomba_death_time = 0
GOOMBA_RESPAWN_DELAY = 5000
goomba_spawning = False
goomba_spawn_timer = 0

# --- ГУМБРАТ (Goombrat) ---
goombrat_w, goombrat_h = goombrat_frames_right[0].get_width(), goombrat_frames_right[0].get_height()
GOOMBRAT_START_X, GOOMBRAT_START_Y = 176, 320
goombrat_x, goombrat_y = GOOMBRAT_START_X, GOOMBRAT_START_Y
goombrat_dx = 1.2
goombrat_dy = 0.0
goombrat_alive = True
goombrat_gravity = 0.6
goombrat_rect = pygame.Rect(goombrat_x, goombrat_y, goombrat_w, goombrat_h)

goombrat_anim_idx = 0
goombrat_anim_timer = 0
GOOMBRAT_ANIM_SPEED = 10

# === СИСТЕМА СОСТОЯНИЙ МАРИО ===
MARIO_STATE_NORMAL = "normal"
MARIO_STATE_DYING = "dying"
MARIO_STATE_BLACK_SCREEN = "black_screen"
mario_state = MARIO_STATE_NORMAL

# Таймеры для анимации смерти
death_start_time = 0
black_screen_start_time = 0

def reset_level():
    """Сбрасывает уровень к начальному состоянию"""
    global x, y, y_velocity, facing_right, mario_state, is_on_ground, jump_buffer, mario_dx
    global goomba_x, goomba_y, goomba_dx, goomba_dy, goomba_alive, goomba_spawning, goomba_spawn_timer
    global goombrat_x, goombrat_y, goombrat_dx, goombrat_dy, goombrat_alive
    global death_start_time, black_screen_start_time
    global score, score_text
    
    score = 0
    score_text = font.render(f"Goomba count: {score}", True, WHITE)
    
    x, y = START_X, START_Y
    y_velocity = 0
    facing_right = True
    mario_state = MARIO_STATE_NORMAL
    is_on_ground = False
    jump_buffer = 0
    mario_dx = 0.0  # --- НОВОЕ: Сбрасываем инерцию ---
    
    goomba_x, goomba_y = GOOMBA_START_X, GOOMBA_START_Y
    goomba_dx = -1.2
    goomba_dy = 0.0
    goomba_alive = True
    goomba_spawning = False
    goomba_spawn_timer = 0
    goomba_rect.topleft = (goomba_x, goomba_y)
    
    goombrat_x, goombrat_y = GOOMBRAT_START_X, GOOMBRAT_START_Y
    goombrat_dx = 1.2
    goombrat_dy = 0.0
    goombrat_alive = True
    goombrat_rect.topleft = (goombrat_x, goombrat_y)
    
    death_start_time = 0
    black_screen_start_time = 0

    try:
        pygame.mixer.music.rewind()
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        pass

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # ЛОГИКА МАРИО
    if mario_state == MARIO_STATE_NORMAL:
        # --- НОВОЕ: Горизонтальное движение с инерцией (механика льда) ---
        max_speed = 4 if keys[pygame.K_x] else 3
        
        # Проверяем, стоит ли Марио на льду (сенсор под ногами)
        is_on_ice = False
        feet_rect = pygame.Rect(x + 2, y + h, w - 4, 2) # Немного сужаем, чтобы избежать ложных срабатываний
        for solid in solids:
            if feet_rect.colliderect(solid) and solid in ice_blocks:
                is_on_ice = True
                break

        # Настройки физики: на льду ускорение и трение минимальны
        if is_on_ice:
            accel = 0.1      # Медленный разгон
            friction = 0.02  # Очень скользко (долгое торможение)
            turn_brake = 0.15 # Плавный разворот
        else:
            accel = 0.8      # Мгновенный отклик
            friction = 0.8   # Быстрая остановка
            turn_brake = 1.2

        # Применяем ускорение или трение
        if keys[pygame.K_LEFT]:
            if mario_dx > 0: mario_dx -= turn_brake
            else: mario_dx -= accel
            if mario_dx < -max_speed: mario_dx = -max_speed
            facing_right = False
        elif keys[pygame.K_RIGHT]:
            if mario_dx < 0: mario_dx += turn_brake
            else: mario_dx += accel
            if mario_dx > max_speed: mario_dx = max_speed
            facing_right = True
        else:
            if mario_dx > 0:
                mario_dx -= friction
                if mario_dx < 0: mario_dx = 0
            elif mario_dx < 0:
                mario_dx += friction
                if mario_dx > 0: mario_dx = 0

        dx = mario_dx
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
                    mario_dx = 0  # --- НОВОЕ: Останавливаем инерцию при ударе о стену ---
                elif dx < 0:
                    x = solid.right
                    mario_dx = 0
                mario_rect.x = x
                break

        # --- Вертикальное движение ---
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
                break

        if mario_rect.colliderect(box_rect):
            if y_velocity > 0 and prev_mario_rect.bottom <= box_rect.top:
                y = box_rect.top - h
                y_velocity = 0
                is_on_ground = True
                jump_buffer = 0
                mario_rect.y = y

        x = max(0, min(x, WIDTH - w))
        
        if y > HEIGHT + 10:
            mario_state = MARIO_STATE_DYING
            death_start_time = current_time
            y_velocity = 0
            if death_sound:
                death_sound.play()
            pygame.mixer.music.stop()

    elif mario_state == MARIO_STATE_DYING:
        time_since_death = current_time - death_start_time
        
        if time_since_death < 1000:
            y_velocity = 0
        else:
            if time_since_death < 1050:
                y_velocity = -7
            y_velocity += gravity
            y += y_velocity
        
        if y > HEIGHT + 50:
            mario_state = MARIO_STATE_BLACK_SCREEN
            black_screen_start_time = pygame.time.get_ticks()

    elif mario_state == MARIO_STATE_BLACK_SCREEN:
        if current_time - black_screen_start_time >= 2000:
            reset_level()

    # ЛОГИКА ГУМБЫ (Без изменений)
    if goomba_alive:
        goomba_anim_timer += 1
        if goomba_anim_timer >= GOOMBA_ANIM_SPEED:
            goomba_anim_idx = (goomba_anim_idx + 1) % len(goomba_frames_right)
            goomba_anim_timer = 0

        if goomba_spawning:
            goomba_spawn_timer += 1
            target_y = pipe_rect.top - goomba_h
            
            if goomba_y > target_y:
                goomba_y -= 2.5
            else:
                goomba_y = target_y
            goomba_rect.y = goomba_y

            if goomba_spawn_timer >= 30:
                goomba_spawning = False
                goomba_dy = 0
                goomba_rect.y = goomba_y
        else:
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
                    break

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
                    break

            if goomba_x <= 0:
                goomba_x = 0
                goomba_dx = abs(goomba_dx)
            elif goomba_x + goomba_w >= WIDTH:
                goomba_x = WIDTH - goomba_w
                goomba_dx = -abs(goomba_dx)

            if goomba_y > HEIGHT + 50:
                goomba_x, goomba_y = GOOMBA_START_X, 0
                goomba_dx = -1.2
                goomba_dy = 0
                goomba_rect.topleft = (goomba_x, goomba_y)

        if mario_state == MARIO_STATE_NORMAL and not goomba_spawning:
            mario_rect_now = pygame.Rect(x, y, w, h)
            if mario_rect_now.colliderect(goomba_rect):
                prev_mario_bottom = (y - y_velocity) + h
                if y_velocity > 0 and prev_mario_bottom <= goomba_rect.top + 12:
                    goomba_alive = False
                    goomba_death_time = pygame.time.get_ticks()
                    y_velocity = -5
                    
                    score += 1
                    score_text = font.render(f"Goomba count: {score}", True, WHITE)
                    
                    if jump_sound:
                        jump_sound.play()
                else:
                    mario_state = MARIO_STATE_DYING
                    death_start_time = current_time
                    y_velocity = 0
                    if death_sound:
                        death_sound.play()
                    pygame.mixer.music.stop()
                    print("💀 Марио коснулся Гумбы!")

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

    # ЛОГИКА ГУМБРАТА (Goombrat) (Без изменений)
    if goombrat_alive:
        goombrat_anim_timer += 1
        if goombrat_anim_timer >= GOOMBRAT_ANIM_SPEED:
            goombrat_anim_idx = (goombrat_anim_idx + 1) % len(goombrat_frames_right)
            goombrat_anim_timer = 0

        goombrat_x += goombrat_dx
        goombrat_rect.x = goombrat_x
        
        for solid in solids:
            if goombrat_rect.colliderect(solid):
                if goombrat_dx > 0:
                    goombrat_x = solid.left - goombrat_w
                elif goombrat_dx < 0:
                    goombrat_x = solid.right
                goombrat_dx = -goombrat_dx
                goombrat_rect.x = goombrat_x
                break

        goombrat_dy += goombrat_gravity
        goombrat_y += goombrat_dy
        goombrat_rect.y = goombrat_y
        
        for solid in solids:
            if goombrat_rect.colliderect(solid):
                if goombrat_dy > 0:
                    goombrat_y = solid.top - goombrat_h
                    goombrat_dy = 0
                elif goombrat_dy < 0:
                    goombrat_y = solid.bottom
                    goombrat_dy = 0
                goombrat_rect.y = goombrat_y
                break

        if goombrat_dy == 0: 
            sensor_rect = pygame.Rect(0, 0, 2, 2)
            if goombrat_dx < 0:
                sensor_rect.topleft = (goombrat_rect.left - 2, goombrat_rect.bottom)
            else:
                sensor_rect.topright = (goombrat_rect.right + 2, goombrat_rect.bottom)
            
            on_edge = True
            for solid in solids:
                if sensor_rect.colliderect(solid):
                    on_edge = False
                    break
                    
            if on_edge:
                goombrat_dx = -goombrat_dx

        if goombrat_x <= 0:
            goombrat_x = 0
            goombrat_dx = abs(goombrat_dx)
        elif goombrat_x + goombrat_w >= WIDTH:
            goombrat_x = WIDTH - goombrat_w
            goombrat_dx = -abs(goombrat_dx)
        goombrat_rect.x = goombrat_x

        if mario_state == MARIO_STATE_NORMAL:
            mario_rect_now = pygame.Rect(x, y, w, h)
            if mario_rect_now.colliderect(goombrat_rect):
                prev_mario_bottom = (y - y_velocity) + h
                if y_velocity > 0 and prev_mario_bottom <= goombrat_rect.top + 12:
                    goombrat_alive = False  # Goombrat умирает навсегда
                    y_velocity = -5
                    score += 1
                    score_text = font.render(f"Goomba count: {score}", True, WHITE)
                    if jump_sound: jump_sound.play()
                else:
                    mario_state = MARIO_STATE_DYING
                    death_start_time = current_time
                    y_velocity = 0
                    if death_sound: death_sound.play()
                    pygame.mixer.music.stop()

    # ОТРИСОВКА
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((107, 140, 255))

    for t_rect in tile_rects:
        screen.blit(tile_surface, t_rect.topleft)

    # --- НОВОЕ: Отрисовка ледяных блоков ---
    for ice in ice_blocks:
        for ix in range(ice.left, ice.right, 16):
            screen.blit(ice_block_scaled, (ix, ice.top))

    screen.blit(box_img, box_rect.topleft)
    
    # --- ИСПРАВЛЕНИЕ: Отрисовка def_blocks циклом ---
    for b in def_blocks:
        for bx in range(b.left, b.right, 16):  # Шаг 16 пикселей
            screen.blit(def_block_scaled, (bx, b.top))
    
    screen.blit(warp_pipe, pipe_rect.topleft)
    screen.blit(mini_pip, pipe_mini.topleft)

    if goomba_alive:
        frames = goomba_frames_right if goomba_dx > 0 else goomba_frames_left
        screen.blit(frames[goomba_anim_idx], (goomba_x, goomba_y))

    if goombrat_alive:
        frames = goombrat_frames_right if goombrat_dx > 0 else goombrat_frames_left
        screen.blit(frames[goombrat_anim_idx], (goombrat_x, goombrat_y))

    if mario_state == MARIO_STATE_DYING:
        screen.blit(mario_death, (x, y))
    elif mario_state == MARIO_STATE_NORMAL:
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

    if mario_state == MARIO_STATE_BLACK_SCREEN:
        screen.fill((0, 0, 0))

    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()