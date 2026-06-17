import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

# --- Настройки окна ---
WIDTH, HEIGHT = 512, 432
score = 0
lives = 3
coins_collected = 0
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score_text = font.render(f"Lives: {lives}  Coins: {coins_collected}  Enemies: {score}", True, WHITE)
pygame.display.set_caption("Super Mario World")

def update_hud():
    global score_text
    score_text = font.render(f"Lives: {lives}  Coins: {coins_collected}  Enemies: {score}", True, WHITE)

def load_image(path):
    if not os.path.exists(path):
        print(f"❌ Ошибка: файл '{path}' не найден!")
        return pygame.Surface((16, 16), pygame.SRCALPHA)
    img = pygame.image.load(path)
    return img.convert_alpha()

try:
    warp_pipe = load_image('./assets/Warp_Pipe_SMW.png')
    tile_img = load_image('./assets/ground.png')
    box_img = load_image('./assets/box.png')
    def_block = load_image('./assets/SMW_RotatingBlock.png')
    mini_pip = load_image('./assets/mini_pipe.png')
    ice_block = load_image('./assets/IceBlock.png')
    plus_live_mushroom = load_image('./assets/1-up.png')
    coin_img = load_image('./assets/coin.png')
    tencoin = load_image('./assets/10coin.png')
    coin_img_scaled = pygame.transform.scale(coin_img, (16, 16))
    tencoin_img_scaled = pygame.transform.scale(tencoin, (32, 32))
    green_mushroom_img = pygame.transform.scale(plus_live_mushroom, (16, 16))
    def_block_scaled = pygame.transform.scale(def_block, (16, 16))

    # Выбор персонажа
    Select_Mario = load_image('./assets/Mario/Mario_select.png')
    Select_Luigi = load_image('./assets/Luigi/Luigi_select.png')
    Select_Toad = load_image('./assets/Toad/Toad_select.png')
    Select_Toadsworth = load_image('./assets/Toadsworth/Toadsworth_select.png')

    # Спрайты Луиджи
    Luigi_idle = load_image('./assets/Luigi/idle.png')
    Luigi_jump = load_image('./assets/Luigi/jump.png')
    Luigi_up = load_image('./assets/Luigi/up.png')
    Luigi_down = load_image('./assets/Luigi/down.png')
    Luigi_fall = load_image('./assets/Luigi/fall.png')
    Luigi_death_raw = load_image('./assets/Luigi/death.png')
    Luigi_walk_frames_right = [load_image('./assets/Luigi/walk1.png'), load_image('./assets/Luigi/walk2.png')]

    # Спрайты Тоада
    Toad_idle = load_image('./assets/Toad/idle.png')
    Toad_jump = load_image('./assets/Toad/jump.png')
    Toad_up = load_image('./assets/Toad/up.png')
    Toad_down = load_image('./assets/Toad/down.png')
    Toad_fall = load_image('./assets/Toad/fall.png')
    Toad_death_raw = load_image('./assets/Toad/death.png')
    Toad_walk_frames_right = [load_image('./assets/Toad/walk1.png'), load_image('./assets/Toad/walk2.png')]

    # Спрайты Toadsworth
    Toadsworth_idle = load_image('./assets/Toadsworth/idle.png')
    Toadsworth_jump = load_image('./assets/Toadsworth/jump.png')
    Toadsworth_up = load_image('./assets/Toadsworth/up.png')
    Toadsworth_down = load_image('./assets/Toadsworth/down.png')
    Toadsworth_fall = load_image('./assets/Toadsworth/fall.png')
    Toadsworth_death_raw = load_image('./assets/Toadsworth/death.png')
    Toadsworth_walk_frames_right = [load_image('./assets/Toadsworth/walk1.png'), load_image('./assets/Toadsworth/walk2.png')]
    
    #Спрайты Марио
    try:
        original_image = load_image("./assets/Mario/SMWSmallMarioSprite.png")
        mario_jump = load_image('./assets/Mario/SMWSmallMarioJumpSprite.png')
        mario_death_raw = load_image('./assets/Mario/Mario_SMW_dying_sprite.png')
        mario_fall = load_image('./assets/Mario/fall.png')
        mario_up = load_image('./assets/Mario/up.png')
        mario_down = load_image('./assets/Mario/down.png')
        mario_walk_frames_right = [load_image('./assets/Mario/marioWalk1.png'), load_image('./assets/Mario/marioWalk2.png'),]
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

# --- Загрузка звуков ---
jump_sound = None
death_sound = None
coin_sound = None
oneup_sound = None

try:
    jump_sound = pygame.mixer.Sound('jump_sound.wav')
except pygame.error as e:
    print("⚠️ Не удалось загрузить jump_sound.wav:", e)

try:
    death_sound = pygame.mixer.Sound('PlayerDown.mp3')
except pygame.error as e:
    print("⚠️ Не удалось загрузить PlayerDown.mp3:", e)

try:
    coin_sound = pygame.mixer.Sound('coin.mp3')
except pygame.error as e:
    print("⚠️ Не удалось загрузить coin.mp3:", e)

try:
    oneup_sound = pygame.mixer.Sound('1up.wav')
except pygame.error as e:
    print("⚠️ Не удалось загрузить 1up.wav:", e)

# --- Загрузка фоновой музыки ---
music_loaded = False
try:
    pygame.mixer.music.load('overworld.wav')
    music_loaded = True
except pygame.error as e:
    print("⚠️ Не удалось загрузить фоновую музыку:", e)

# --- Спрайты персонажей ---
mario_sprites = {'right': original_image, 'left': pygame.transform.flip(original_image, True, False), 'jump_right': mario_jump, 'jump_left': pygame.transform.flip(mario_jump, True, False), 'fall_right': mario_fall, 'fall_left': pygame.transform.flip(mario_fall, True, False), 'up_right': mario_up, 'up_left': pygame.transform.flip(mario_up, True, False), 'down_right': mario_down, 'down_left': pygame.transform.flip(mario_down, True, False), 'death': mario_death_raw, 'walk_right': mario_walk_frames_right, 'walk_left': [pygame.transform.flip(img, True, False) for img in mario_walk_frames_right]}

luigi_sprites = {'right': Luigi_idle, 'left': pygame.transform.flip(Luigi_idle, True, False), 'jump_right': Luigi_jump, 'jump_left': pygame.transform.flip(Luigi_jump, True, False), 'fall_right': Luigi_fall, 'fall_left': pygame.transform.flip(Luigi_fall, True, False), 'up_right': Luigi_up, 'up_left': pygame.transform.flip(Luigi_up, True, False), 'down_right': Luigi_down, 'down_left': pygame.transform.flip(Luigi_down, True, False), 'death': Luigi_death_raw, 'walk_right': Luigi_walk_frames_right, 'walk_left': [pygame.transform.flip(img, True, False) for img in Luigi_walk_frames_right]}

# Спрайты Тоада
toad_sprites = {'right': Toad_idle, 'left': pygame.transform.flip(Toad_idle, True, False), 'jump_right': Toad_jump, 'jump_left': pygame.transform.flip(Toad_jump, True, False), 'fall_right': Toad_fall, 'fall_left': pygame.transform.flip(Toad_fall, True, False), 'up_right': Toad_up, 'up_left': pygame.transform.flip(Toad_up, True, False), 'down_right': Toad_down, 'down_left': pygame.transform.flip(Toad_down, True, False), 'death': Toad_death_raw, 'walk_right': Toad_walk_frames_right, 'walk_left': [pygame.transform.flip(img, True, False) for img in Toad_walk_frames_right]}

# Спрайты Toadsworth
toadsworth_sprites = {'right': Toadsworth_idle, 'left': pygame.transform.flip(Toadsworth_idle, True, False), 'jump_right': Toadsworth_jump, 'jump_left': pygame.transform.flip(Toadsworth_jump, True, False), 'fall_right': Toadsworth_fall, 'fall_left': pygame.transform.flip(Toadsworth_fall, True, False), 'up_right': Toadsworth_up, 'up_left': pygame.transform.flip(Toadsworth_up, True, False), 'down_right': Toadsworth_down, 'down_left': pygame.transform.flip(Toadsworth_down, True, False), 'death': Toadsworth_death_raw, 'walk_right': Toadsworth_walk_frames_right, 'walk_left': [pygame.transform.flip(img, True, False) for img in Toadsworth_walk_frames_right]}

current_sprites = mario_sprites

# --- Начальные параметры скорости и инерции (задаются по умолчанию для Марио) ---
base_max_speed = 3
run_max_speed = 4
base_accel = 0.8
base_friction = 0.8
base_turn_brake = 1.2

# --- Начальные позиции для сброса уровня ---
START_X, START_Y = 100, 384
x, y = START_X, START_Y
w, h = original_image.get_width(), original_image.get_height()
facing_right = True

# --- Переменная для инерции (текущая горизонтальная скорость) ---
mario_dx = 0.0
mario_anim_idx = 0          
mario_anim_timer = 0        
MARIO_WALK_SPEED = 10       

pipe_rect = warp_pipe.get_rect(topleft=(400, 384))
pipe_mini = mini_pip.get_rect(topleft=(160, 400))

def_blocks = [pygame.Rect(112, 336, 96, 16)]

box_rect = box_img.get_rect(topleft=(0, 384))

tile_size = 16
tile_size_r = 208
tile_rects = [pygame.Rect(tx, HEIGHT - tile_size, tile_size, tile_size) for tx in range(0, WIDTH, tile_size)]
tile_surface = pygame.transform.scale(tile_img, (tile_size_r, tile_size))

# --- Ледяные блоки ---
ice_blocks = [pygame.Rect(208, 336, 64, 16)]
solids = tile_rects + [pipe_rect] + def_blocks + [pipe_mini] + ice_blocks

ice_block_scaled = pygame.transform.scale(ice_block, (16, 16))

y_velocity = 0
gravity = 0.6
jump_power = -6
is_on_ground = False
jump_buffer = 0
MAX_JUMP_BUFFER = 8

# --- ГОМБА (Goomba) ---
goomba_w, goomba_h = goomba_frames_right[0].get_width(), goomba_frames_right[0].get_height()
GOOMBA_START_X, GOOMBA_START_Y = 176, 320
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

# === СИСТЕМА СОСТОЯНИЙ ===
MARIO_STATE_SELECT = "select"
MARIO_STATE_NORMAL = "normal"
MARIO_STATE_DYING = "dying"
MARIO_STATE_BLACK_SCREEN = "black_screen"
MARIO_STATE_GAME_OVER = "game_over"
mario_state = MARIO_STATE_SELECT
current_selection = 0

# Таймеры для анимации смерти
death_start_time = 0
black_screen_start_time = 0

# --- Монеты ---
initial_coins = [pygame.Rect(120, 300, 16, 16), pygame.Rect(140, 300, 16, 16), pygame.Rect(160, 300, 16, 16), pygame.Rect(250, 280, 16, 16), pygame.Rect(300, 350, 16, 16),]
coins = initial_coins[:]

# --- 10-монеты (дают 10 монет за подбор) ---
initial_ten_coins = [pygame.Rect(350, 300, 16, 16), pygame.Rect(420, 280, 16, 16)]
ten_coins = initial_ten_coins[:]

# --- гриб 1-Up ---
class GreenMushroom:
    def __init__(self, x, y, dx=1.5):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.dx = dx
        self.dy = 0.0
        self.gravity = 0.6
        self.alive = True
        
    def update(self, solids):
        if not self.alive:
            return
            
        self.rect.x += self.dx
        
        for solid in solids:
            if self.rect.colliderect(solid):
                if self.dx > 0:
                    self.rect.right = solid.left
                    self.dx = -self.dx
                elif self.dx < 0:
                    self.rect.left = solid.right
                    self.dx = -self.dx
                break
        
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = abs(self.dx)
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.dx = -abs(self.dx)
        
        self.dy += self.gravity
        self.rect.y += self.dy
        
        for solid in solids:
            if self.rect.colliderect(solid):
                if self.dy > 0:
                    self.rect.bottom = solid.top
                    self.dy = 0
                elif self.dy < 0:
                    self.rect.top = solid.bottom
                    self.dy = 0
                break
        
        if self.rect.top > HEIGHT + 50:
            self.alive = False

initial_mushrooms = [(350, 280, 1.5)]
green_mushrooms = [GreenMushroom(x, y, dx) for x, y, dx in initial_mushrooms]

def reset_level():
    global x, y, y_velocity, facing_right, mario_state, is_on_ground, jump_buffer, mario_dx
    global goomba_x, goomba_y, goomba_dx, goomba_dy, goomba_alive, goomba_spawning, goomba_spawn_timer
    global goombrat_x, goombrat_y, goombrat_dx, goombrat_dy, goombrat_alive
    global death_start_time, black_screen_start_time
    global score, coins, coins_collected, green_mushrooms, ten_coins
    
    score = 0
    coins.clear()
    coins.extend(initial_coins)
    ten_coins.clear()
    ten_coins.extend(initial_ten_coins)
    coins_collected = 0
    
    green_mushrooms = [GreenMushroom(x, y, dx) for x, y, dx in initial_mushrooms]
    
    update_hud()
    
    x, y = START_X, START_Y
    y_velocity = 0
    facing_right = True
    mario_state = MARIO_STATE_NORMAL
    is_on_ground = False
    jump_buffer = 0
    mario_dx = 0.0 
    
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

def reset_game():
    global lives, score, coins_collected, mario_state
    global coins, green_mushrooms, ten_coins
    
    lives = 3
    score = 0
    coins_collected = 0
    
    coins.clear()
    coins.extend(initial_coins)
    
    ten_coins.clear()
    ten_coins.extend(initial_ten_coins)
    
    green_mushrooms.clear()
    green_mushrooms.extend([GreenMushroom(x, y, dx) for x, y, dx in initial_mushrooms])
    
    update_hud()
    
    # Переход на экран выбора
    mario_state = MARIO_STATE_SELECT

def start_music():
    """Запуск фоновой музыки"""
    if music_loaded:
        try:
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.4)
        except pygame.error:
            pass

clock = pygame.time.Clock()
running = True

# Запуск музыки при старте (для экрана выбора)
start_music()
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # --- ПОЛНЫЙ ПЕРЕЗАПУСК ИГРЫ ПО F2 (возврат к выбору персонажа) ---
            if event.key == pygame.K_F2:
                reset_game()
                start_music()
                continue

            # Логика выбора персонажа
            if mario_state == MARIO_STATE_SELECT:
                if event.key == pygame.K_LEFT:
                    current_selection = (current_selection - 1) % 4
                elif event.key == pygame.K_RIGHT:
                    current_selection = (current_selection + 1) % 4
                elif event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                    if current_selection == 0:
                        current_sprites = mario_sprites
                        jump_power = -6
                        base_max_speed = 3
                        run_max_speed = 4
                        base_accel = 0.8
                        base_friction = 0.8
                        base_turn_brake = 1.2
                        MARIO_WALK_SPEED = 10
                    elif current_selection == 1:
                        current_sprites = luigi_sprites
                        jump_power = -7.5
                        base_max_speed = 3
                        run_max_speed = 4
                        base_accel = 0.8
                        base_friction = 0.8
                        base_turn_brake = 1.2
                        MARIO_WALK_SPEED = 10
                    elif current_selection == 2:  # Тоад
                        current_sprites = toad_sprites
                        jump_power = -6
                        base_max_speed = 4
                        run_max_speed = 5
                        base_accel = 1.0
                        base_friction = 0.9
                        base_turn_brake = 1.4
                        MARIO_WALK_SPEED = 7
                    else:  # Toadsworth - скорость и прыжок чуть ниже Марио
                        current_sprites = toadsworth_sprites
                        jump_power = -5.5
                        base_max_speed = 2.5
                        run_max_speed = 3.5
                        base_accel = 0.7
                        base_friction = 0.75
                        base_turn_brake = 1.1
                        MARIO_WALK_SPEED = 11
                    w, h = current_sprites['right'].get_width(), current_sprites['right'].get_height()
                    reset_level()
                    start_music()
            
            # --- После Game Over - возврат на экран выбора ---
            elif mario_state == MARIO_STATE_GAME_OVER:
                if event.key == pygame.K_r:
                    reset_game()
                    start_music()
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if mario_state == MARIO_STATE_SELECT:
        if music_loaded and not pygame.mixer.music.get_busy():
            start_music()

    # ЛОГИКА МАРИО
    if mario_state == MARIO_STATE_NORMAL:
        # --- Горизонтальное движение с инерцией (механика льда) ---
        max_speed = run_max_speed if keys[pygame.K_x] else base_max_speed
        
        is_on_ice = False
        feet_rect = pygame.Rect(x + 2, y + h, w - 4, 2)
        for solid in solids:
            if feet_rect.colliderect(solid) and solid in ice_blocks:
                is_on_ice = True
                break

        if is_on_ice:
            accel = 0.1
            friction = 0.02
            turn_brake = 0.15
        else:
            accel = base_accel
            friction = base_friction
            turn_brake = base_turn_brake

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
                mario_anim_idx = (mario_anim_idx + 1) % len(current_sprites['walk_right'])
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
                    mario_dx = 0
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
        
        # --- Сбор обычных монет ---
        mario_rect_now = pygame.Rect(x, y, w, h)
        for coin in coins[:]:
            if mario_rect_now.colliderect(coin):
                coins.remove(coin)
                coins_collected += 1
                
                if coin_sound:
                    coin_sound.play()
                
                if coins_collected >= 100:
                    coins_collected -= 100
                    lives += 1
                    
                update_hud()

        # --- Сбор 10-монет ---
        for tcoin in ten_coins[:]:
            if mario_rect_now.colliderect(tcoin):
                ten_coins.remove(tcoin)
                coins_collected += 10
                
                if coin_sound:
                    coin_sound.play()
                    
                update_hud()

        # --- Сбор гриба 1-Up ---
        for mushroom in green_mushrooms[:]:
            if mushroom.alive and mario_rect_now.colliderect(mushroom.rect):
                mushroom.alive = False
                lives += 1
                if oneup_sound:
                    oneup_sound.play()
                update_hud()

        # --- Падение в пропасть ---
        if y > HEIGHT + 10:
            if lives > 0:
                lives -= 1
                mario_state = MARIO_STATE_DYING
                death_start_time = current_time
                y_velocity = 0
                if death_sound: death_sound.play()
                pygame.mixer.music.stop()
                update_hud()
            else:
                # --- Переход на Game Over при 0 жизнях ---
                mario_state = MARIO_STATE_GAME_OVER
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
            # --- Проверка жизней после анимации смерти ---
            if lives > 0:
                reset_level()
                start_music()
            else:
                mario_state = MARIO_STATE_GAME_OVER

    elif mario_state == MARIO_STATE_GAME_OVER:
        pass

    # ЛОГИКА ВРАГОВ
    if mario_state == MARIO_STATE_NORMAL:
        # --- ФИЗИКА ГРИБОВ 1-UP (ТЕПЕРЬ ОНИ ОСТАНАВЛИВАЮТСЯ ПРИ СМЕРТИ, КАК ГУМБА) ---
        for mushroom in green_mushrooms:
            mushroom.update(solids)
        
        green_mushrooms = [m for m in green_mushrooms if m.alive]

        # ЛОГИКА ГУМБЫ
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

            if not goomba_spawning:
                mario_rect_now = pygame.Rect(x, y, w, h)
                if mario_rect_now.colliderect(goomba_rect):
                    prev_mario_bottom = (y - y_velocity) + h
                    if y_velocity > 0 and prev_mario_bottom <= goomba_rect.top + 12:
                        goomba_alive = False
                        goomba_death_time = pygame.time.get_ticks()
                        y_velocity = -5
                        
                        score += 1
                        update_hud()
                        
                        if jump_sound: jump_sound.play()
                    else:
                        if lives > 0:
                            lives -= 1
                            mario_state = MARIO_STATE_DYING
                            death_start_time = current_time
                            y_velocity = 0
                            if death_sound: death_sound.play()
                            pygame.mixer.music.stop()
                            update_hud()
                        else:
                            mario_state = MARIO_STATE_GAME_OVER
                            pygame.mixer.music.stop()

        # ЛОГИКА ГУМБРАТА (Goombrat)
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

            mario_rect_now = pygame.Rect(x, y, w, h)
            if mario_rect_now.colliderect(goombrat_rect):
                prev_mario_bottom = (y - y_velocity) + h
                if y_velocity > 0 and prev_mario_bottom <= goombrat_rect.top + 12:
                    goombrat_alive = False
                    y_velocity = -5
                    score += 1
                    update_hud()
                    if jump_sound: jump_sound.play()
                else:
                    if lives > 0:
                        lives -= 1
                        mario_state = MARIO_STATE_DYING
                        death_start_time = current_time
                        y_velocity = 0
                        if death_sound: death_sound.play()
                        pygame.mixer.music.stop()
                        update_hud()
                    else:
                        mario_state = MARIO_STATE_GAME_OVER
                        pygame.mixer.music.stop()

    # ОТРИСОВКА
    if mario_state == MARIO_STATE_SELECT:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill((107, 140, 255))
            
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("SELECT YOUR CHARACTER", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
        
        # Четыре персонажа на экране выбора
        mario_select_rect = Select_Mario.get_rect(center=(WIDTH//8, HEIGHT//2))
        luigi_select_rect = Select_Luigi.get_rect(center=(3*WIDTH//8, HEIGHT//2))
        toad_select_rect = Select_Toad.get_rect(center=(5*WIDTH//8, HEIGHT//2))
        toadsworth_select_rect = Select_Toadsworth.get_rect(center=(7*WIDTH//8, HEIGHT//2))
        
        screen.blit(Select_Mario, mario_select_rect)
        screen.blit(Select_Luigi, luigi_select_rect)
        screen.blit(Select_Toad, toad_select_rect)
        screen.blit(Select_Toadsworth, toadsworth_select_rect)
        
        select_rects = [mario_select_rect, luigi_select_rect, toad_select_rect, toadsworth_select_rect]
        names = ["MARIO", "LUIGI", "TOAD", "TOADSWORTH"]
        colors = [(255, 255, 0), (0, 255, 0), (255, 100, 100), (255, 200, 150)]  # жёлтый, зелёный, красноватый, бежевый
        
        for i, rect in enumerate(select_rects):
            if current_selection == i:
                pygame.draw.rect(screen, colors[i], rect.inflate(20, 20), 5)
            name_text = font.render(names[i], True, WHITE)
            screen.blit(name_text, (rect.centerx - name_text.get_width()//2, rect.bottom + 20))
            
        hint_text = font.render("Use LEFT/RIGHT and press Z/ENTER", True, WHITE)
        screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT - 50))
        
    else:
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill((107, 140, 255))

        for t_rect in tile_rects:
            screen.blit(tile_surface, t_rect.topleft)

        for ice in ice_blocks:
            for ix in range(ice.left, ice.right, 16):
                screen.blit(ice_block_scaled, (ix, ice.top))

        screen.blit(box_img, box_rect.topleft)
        
        for b in def_blocks:
            for bx in range(b.left, b.right, 16):
                screen.blit(def_block_scaled, (bx, b.top))
        
        screen.blit(warp_pipe, pipe_rect.topleft)
        screen.blit(mini_pip, pipe_mini.topleft)

        # Отрисовка
        for coin in coins:
            screen.blit(coin_img_scaled, coin.topleft)

        for tcoin in ten_coins:
            screen.blit(tencoin_img_scaled, tcoin.topleft)

        for mushroom in green_mushrooms:
            if mushroom.alive:
                screen.blit(green_mushroom_img, mushroom.rect.topleft)

        if goomba_alive:
            frames = goomba_frames_right if goomba_dx > 0 else goomba_frames_left
            screen.blit(frames[goomba_anim_idx], (goomba_x, goomba_y))

        if goombrat_alive:
            frames = goombrat_frames_right if goombrat_dx > 0 else goombrat_frames_left
            screen.blit(frames[goombrat_anim_idx], (goombrat_x, goombrat_y))

        if mario_state == MARIO_STATE_DYING:
            screen.blit(current_sprites['death'], (x, y))
        elif mario_state == MARIO_STATE_NORMAL:
            if not is_on_ground:
                if y_velocity < 0:
                    current_sprite = current_sprites['jump_right'] if facing_right else current_sprites['jump_left']
                else:
                    current_sprite = current_sprites['fall_right'] if facing_right else current_sprites['fall_left']
            else:
                if is_moving:
                    frames = current_sprites['walk_right'] if facing_right else current_sprites['walk_left']
                    current_sprite = frames[mario_anim_idx]
                elif keys[pygame.K_UP]:
                    current_sprite = current_sprites['up_right'] if facing_right else current_sprites['up_left']
                elif keys[pygame.K_DOWN]:
                    current_sprite = current_sprites['down_right'] if facing_right else current_sprites['down_left']
                else:
                    current_sprite = current_sprites['right'] if facing_right else current_sprites['left']
            screen.blit(current_sprite, (x, y))

        if mario_state == MARIO_STATE_BLACK_SCREEN:
            screen.fill((0, 0, 0))
            
        if mario_state == MARIO_STATE_GAME_OVER:
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 36))
            
            restart_text = font.render("Press R to return to character select", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

        screen.blit(score_text, (10, 10))
    pygame.display.flip()
pygame.quit()
sys.exit()