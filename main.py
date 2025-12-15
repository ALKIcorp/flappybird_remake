import pygame
import random
import sys
import os
from PIL import Image
import colorsys

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Game Variables
GRAVITY = 0.25
BIRD_MOVEMENT = 0
GAME_ACTIVE = True
SCORE = 0
HIGH_SCORE = 0

# Load Assets
def load_asset(name):
    path = os.path.join('assets', name)
    if not os.path.exists(path):
        print(f"Error: Could not find asset {path}")
        sys.exit()
    
    pil_image = Image.open(path).convert('RGBA')
    image_data = pil_image.tobytes()
    image_size = pil_image.size
    
    return pygame.image.fromstring(image_data, image_size, 'RGBA').convert()

def load_asset_alpha(name, return_pil=False):
    path = os.path.join('assets', name)
    if not os.path.exists(path):
        print(f"Error: Could not find asset {path}")
        sys.exit()
        
    pil_image = Image.open(path).convert('RGBA')
    
    if return_pil:
        return pil_image
        
    image_data = pil_image.tobytes()
    image_size = pil_image.size
    
    return pygame.image.fromstring(image_data, image_size, 'RGBA').convert_alpha()

# Background
BG_SURFACE = load_asset('background-day.png')

# Base
BASE_SURFACE = load_asset('base.png')
BASE_X_POS = 0

# Color Generation Logic
def hue_shift_image(pil_image, hue_shift):
    # Convert RGBA to HSV, shift H, convert back
    # PIL doesn't have direct HSV support for RGBA, so we separate alpha
    r, g, b, a = pil_image.split()
    rgb_image = Image.merge('RGB', (r, g, b))
    hsv_image = rgb_image.convert('HSV')
    
    h, s, v = hsv_image.split()
    np_h = h.point(lambda i: (i + int(hue_shift * 255)) % 255) # Ensure int for point operation
    
    hsv_image = Image.merge('HSV', (np_h, s, v))
    rgb_shifted = hsv_image.convert('RGB')
    
    # Merge back alpha
    r_new, g_new, b_new = rgb_shifted.split()
    return Image.merge('RGBA', (r_new, g_new, b_new, a))

def create_bird_variants():
    base_names = ['bird-down.png', 'bird-mid.png', 'bird-up.png']
    base_images = [load_asset_alpha(name, return_pil=True) for name in base_names]
    
    variants = []
    # Generate 10 colors
    for i in range(10):
        shift = i / 10.0
        colored_frames = []
        for img in base_images:
            # To get specific colors we might need to know base hue, but simple shift gives variety
            new_img = hue_shift_image(img, shift)
            
            # Convert to Pygame Surface
            raw_str = new_img.tobytes()
            raw_size = new_img.size
            surface = pygame.image.fromstring(raw_str, raw_size, 'RGBA').convert_alpha()
            colored_frames.append(surface)
        variants.append(colored_frames)
    return variants

BIRD_VARIANTS = create_bird_variants()
CURRENT_BIRD_COLOR = 0
BIRD_FRAMES = BIRD_VARIANTS[CURRENT_BIRD_COLOR]
BIRD_INDEX = 0
BIRD_SURFACE = BIRD_FRAMES[BIRD_INDEX]
BIRD_RECT = BIRD_SURFACE.get_rect(center = (50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
PIPE_SURFACE = load_asset_alpha('pipe.png')
PIPE_LIST = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
PIPE_HEIGHT = [200, 300, 400]

# Game Over Message
GAMEOVER_SURFACE = load_asset_alpha('gameover.png')
GAMEOVER_RECT = GAMEOVER_SURFACE.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

def draw_base():
    SCREEN.blit(BASE_SURFACE, (BASE_X_POS, 400)) # 512 - 112 = 400 (base height is 112)
    SCREEN.blit(BASE_SURFACE, (BASE_X_POS + SCREEN_WIDTH, 400))

def create_pipe():
    random_pipe_pos = random.choice(PIPE_HEIGHT)
    bottom_pipe = PIPE_SURFACE.get_rect(midtop = (SCREEN_WIDTH + 50, random_pipe_pos))
    top_pipe = PIPE_SURFACE.get_rect(midbottom = (SCREEN_WIDTH + 50, random_pipe_pos - 150)) # 150 is the gap
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5 # Tube speed
    return [pipe for pipe in pipes if pipe.right > -50] # Remove pipes that go off screen

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT: # Bottom pipe
            SCREEN.blit(PIPE_SURFACE, pipe)
        else: # Top pipe
            flip_pipe = pygame.transform.flip(PIPE_SURFACE, False, True)
            SCREEN.blit(flip_pipe, pipe)

def check_collision(pipes):
    global GAME_ACTIVE
    for pipe in pipes:
        if BIRD_RECT.colliderect(pipe):
            return False

    if BIRD_RECT.top <= -100 or BIRD_RECT.bottom >= 400: # 400 is base floor
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -BIRD_MOVEMENT * 3, 1)
    return new_bird

def bird_animation():
    new_bird = BIRD_FRAMES[BIRD_INDEX]
    new_bird_rect = new_bird.get_rect(center = (50, BIRD_RECT.centery))
    return new_bird, new_bird_rect

# Load Score Images
SCORE_IMAGES = {
    '0': load_asset_alpha('0.png'),
    '1': load_asset_alpha('1.png'),
    '2': load_asset_alpha('2.png'),
    '3': load_asset_alpha('3.png'),
    '4': load_asset_alpha('4.png'),
    '5': load_asset_alpha('5.png'),
    '6': load_asset_alpha('6.png'),
    '7': load_asset_alpha('7.png'),
    '8': load_asset_alpha('8.png'),
    '9': load_asset_alpha('9.png')
}

def display_score(score_val, y_pos):
    score_digits = [int(x) for x in list(str(int(score_val)))]
    total_width = 0
    for digit in score_digits:
        total_width += SCORE_IMAGES[str(digit)].get_width()
    
    X_OFFSET = (SCREEN_WIDTH - total_width) / 2
    
    for digit in score_digits:
        SCREEN.blit(SCORE_IMAGES[str(digit)], (X_OFFSET, y_pos))
        X_OFFSET += SCORE_IMAGES[str(digit)].get_width()

def score_display(game_state):
    if game_state == 'main_game':
        display_score(SCORE, 50)
    if game_state == 'game_over':
        display_score(SCORE, 50)
        # High score logic can be just printed to console if font fails or use images too
        # For now let's just show current score. 
        # Or load a "best" image? 
        # The user wants "full game", so I should probably render high score too.
        # I'll render high score below it.
        # display_score(HIGH_SCORE, 400) # Simple

def pipe_score_check():
    global SCORE
    if PIPE_LIST:
        for pipe in PIPE_LIST:
            # speed is 2.5. 50 +/- 1.25 covers the range.
            if 48 < pipe.centerx < 52:
                SCORE += 0.5 
                if int(SCORE) == SCORE: # Only play when score becomes integer (passed both parts or just simplifiction)
                    # Actually pipe list has 2 rects per pipe (top/bottom).
                    # 48-52 range is passed by both.
                    # 0.5 + 0.5 = 1.
                    # If we play sound on every hit, we get double sound.
                    # Let's play only if pipe is bottom pipe to avoid double trigger?
                    # But pipe object doesn't carry 'bottom' info explicitly unless we check coord.
                    if 0 < pipe.centery: # Bottom pipe usually has positive Y center in visible range? 
                        # Top pipe y center is negative or small?
                        # Let's check: bottom pipe midtop is random_pipe_pos (200,300,400).
                        # Screen height 512.
                        # pipe height is huge.
                        # It's safer to check `SCORE % 1 == 0` but `SCORE` is float.
                        if SCORE % 1 == 0:
                             pass

 

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

import math

# Start Screen
GAME_READY_SURFACE = load_asset_alpha('message.png')
GAME_READY_RECT = GAME_READY_SURFACE.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Settings Button
SETTINGS_BTN_RECT = pygame.Rect(SCREEN_WIDTH - 40, 10, 28, 28)
SETTINGS_ANGLE = 0

def draw_settings_button():
    global SETTINGS_ANGLE
    center_x, center_y = SETTINGS_BTN_RECT.centerx, SETTINGS_BTN_RECT.centery
    color = (255, 255, 255) # White
    hole_color = (78, 192, 202) # Sky Blue
    
    # Dimensions based on 28px size (0.7 of 40px)
    bar_len = 28
    bar_thickness = 10 
    fill_radius = 10   
    hole_radius = 6   
    
    # Update Rotation (Spin)
    SETTINGS_ANGLE += 1
    if SETTINGS_ANGLE >= 360:
        SETTINGS_ANGLE = 0
        
    # Draw 3 Bars (Pills)
    # Angles: 0, 60, 120 + rotation
    base_angles = [0, 60, 120]
    
    for base_a in base_angles:
        rad = math.radians(base_a + SETTINGS_ANGLE)
        
        # Calculate Pill Endpoints
        # The bar is centered. Length 40. Extends 20 each way.
        # But we need to draw it as a thick line with rounded caps (circles).
        # Center of rounded caps are at distance (Length/2 - Thickness/2)
        offset_dist = (bar_len / 2) - (bar_thickness / 2)
        
        dx = math.cos(rad) * offset_dist
        dy = math.sin(rad) * offset_dist
        
        p1 = (center_x - dx, center_y - dy)
        p2 = (center_x + dx, center_y + dy)
        
        # Draw thick line
        pygame.draw.line(SCREEN, color, p1, p2, bar_thickness)
        # Draw caps (explicitly if line caps aren't round)
        pygame.draw.circle(SCREEN, color, p1, bar_thickness // 2)
        pygame.draw.circle(SCREEN, color, p2, bar_thickness // 2)

    # Draw Fill Circle
    pygame.draw.circle(SCREEN, color, (center_x, center_y), fill_radius)
    
    # Draw Hole
    pygame.draw.circle(SCREEN, hole_color, (center_x, center_y), hole_radius)

def draw_close_button():
    # Draw Close "X" Icon
    rect = SETTINGS_BTN_RECT
    color = (255, 255, 255)
    width = 4
    
    # Draw X
    # Inset slightly
    inset = 6
    start_pos1 = (rect.left + inset, rect.top + inset)
    end_pos1 = (rect.right - inset, rect.bottom - inset)
    
    start_pos2 = (rect.right - inset, rect.top + inset)
    end_pos2 = (rect.left + inset, rect.bottom - inset)
    
    pygame.draw.line(SCREEN, color, start_pos1, end_pos1, width)
    pygame.draw.line(SCREEN, color, start_pos2, end_pos2, width)

# Game State
# 0: Menu/Ready, 1: Playing, 2: Game Over, 3: Settings
GAME_STATE = 0 
GAME_ACTIVE = False 

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_STATE == 0:
                if SETTINGS_BTN_RECT.collidepoint(event.pos):
                    GAME_STATE = 3
                else:
                    # Start Game on click elsewhere
                    GAME_STATE = 1
                    GAME_ACTIVE = True
                    BIRD_MOVEMENT = 0
                    BIRD_MOVEMENT -= 6
                    PIPE_LIST.clear()
                    BIRD_RECT.center = (50, 256)
                    SCORE = 0
            elif GAME_STATE == 2:
                # Restart
                GAME_STATE = 0
                GAME_ACTIVE = False
                PIPE_LIST.clear()
                BIRD_RECT.center = (50, 256)
                BIRD_MOVEMENT = 0
                SCORE = 0
            elif GAME_STATE == 3:
                # Check for Close Button click
                if SETTINGS_BTN_RECT.collidepoint(event.pos):
                    GAME_STATE = 0
                else:
                    # Check for bird selection click
                    start_x = 40
                    start_y = 100
                    padding = 45
                    
                    for i in range(10):
                        row = i // 5
                        col = i % 5
                        x = start_x + (col * padding)
                        y = start_y + (row * padding * 1.5)
                        
                        # Reconstruct rect for click check (approx size of bird 34x24)
                        item_rect = pygame.Rect(0, 0, 40, 40)
                        item_rect.center = (x, y)
                        
                        if item_rect.collidepoint(event.pos):
                            CURRENT_BIRD_COLOR = i
                            BIRD_FRAMES = BIRD_VARIANTS[CURRENT_BIRD_COLOR]
                            BIRD_SURFACE = BIRD_FRAMES[BIRD_INDEX]
                            # Auto-close on selection? User mostly asked for Close button.
                            # Let's keep it open or close? Typically, selection closes or updates.
                            # Prev behavior was "Exit settings on any click". 
                            # Let's close on selection to proceed to game.
                            GAME_STATE = 0
                            break 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if GAME_STATE == 0:
                    # Start Game
                    GAME_STATE = 1
                    GAME_ACTIVE = True
                    BIRD_MOVEMENT = 0
                    BIRD_MOVEMENT -= 6
                    PIPE_LIST.clear()
                    # Ensure correct bird is loaded
                    BIRD_INDEX = 0
                    BIRD_SURFACE = BIRD_FRAMES[BIRD_INDEX]
                    BIRD_RECT.center = (50, 256)
                    SCORE = 0
                elif GAME_STATE == 1:
                    # Flap
                    BIRD_MOVEMENT = 0
                    BIRD_MOVEMENT -= 6
                elif GAME_STATE == 2:
                    # Restart to Menu
                    GAME_STATE = 0
                    GAME_ACTIVE = False
                    PIPE_LIST.clear()
                    BIRD_RECT.center = (50, 256)
                    BIRD_MOVEMENT = 0
                    SCORE = 0
                elif GAME_STATE == 3:
                    # Select current and go back
                    GAME_STATE = 0

            if event.key == pygame.K_s and GAME_STATE == 0:
                GAME_STATE = 3 # Go to Settings

            if GAME_STATE == 3:
                # Selection logic
                if event.key == pygame.K_RIGHT:
                    CURRENT_BIRD_COLOR = (CURRENT_BIRD_COLOR + 1) % 10
                    BIRD_FRAMES = BIRD_VARIANTS[CURRENT_BIRD_COLOR]
                if event.key == pygame.K_LEFT:
                    CURRENT_BIRD_COLOR = (CURRENT_BIRD_COLOR - 1) % 10
                    BIRD_FRAMES = BIRD_VARIANTS[CURRENT_BIRD_COLOR]
                # Update main bird surface immediately to show preview
                BIRD_SURFACE = BIRD_FRAMES[BIRD_INDEX]

        if event.type == SPAWNPIPE and GAME_ACTIVE:
            PIPE_LIST.extend(create_pipe())

        if event.type == BIRDFLAP and GAME_ACTIVE:
            if BIRD_INDEX < 2:
                BIRD_INDEX += 1
            else:
                BIRD_INDEX = 0
            BIRD_SURFACE, BIRD_RECT = bird_animation()

    # Background
    SCREEN.blit(BG_SURFACE, (0,0))

    if GAME_STATE == 0:
        # Menu / Get Ready
        SCREEN.blit(GAME_READY_SURFACE, GAME_READY_RECT)
        # Bird removed from intro screen as requested
        
        # Draw Settings Button
        draw_settings_button()
        
    elif GAME_STATE == 1:
        # Playing
        GAME_ACTIVE = True # redundant but safe
        BIRD_MOVEMENT += GRAVITY
        BIRD_ROTATED = rotate_bird(BIRD_SURFACE)
        BIRD_RECT.centery += BIRD_MOVEMENT
        SCREEN.blit(BIRD_ROTATED, BIRD_RECT)
        
        game_active_status = check_collision(PIPE_LIST)
        if game_active_status == False:
             GAME_STATE = 2
             GAME_ACTIVE = False
             # DEATH_SOUND.play()

        # Pipes
        PIPE_LIST = move_pipes(PIPE_LIST)
        draw_pipes(PIPE_LIST)
        
        # Score
        pipe_score_check()
        score_display('main_game')
        
    elif GAME_STATE == 2:
        # Game Over
        GAME_ACTIVE = False
        # Still render pipes/bird static?
        draw_pipes(PIPE_LIST)
        BIRD_ROTATED = rotate_bird(BIRD_SURFACE)
        SCREEN.blit(BIRD_ROTATED, BIRD_RECT)
        
        SCREEN.blit(GAMEOVER_SURFACE, GAMEOVER_RECT)
        HIGH_SCORE = update_score(SCORE, HIGH_SCORE)
        score_display('game_over')

    elif GAME_STATE == 3:
        # Settings Screen
        # Show all birds or just current selected?
        # Let's show current selected big in middle
        # text "Settings" (cant do text easily)
        # Show a grid of birds?
        
        # Draw all 10 birds in a grid
        # 2 rows of 5
        start_x = 40
        start_y = 100
        padding = 45
        
        for i in range(10):
            row = i // 5
            col = i % 5
            x = start_x + (col * padding)
            y = start_y + (row * padding * 1.5)
            
            # Draw bird
            # Using midflap for static icon
            bird_icon = BIRD_VARIANTS[i][1] 
            bird_rect_icon = bird_icon.get_rect(center=(x,y))
            SCREEN.blit(bird_icon, bird_rect_icon)
            
            # Highlight selected
            if i == CURRENT_BIRD_COLOR:
                # Draw a rectangle around it? 
                # pygame.draw.rect(SCREEN, (255, 255, 255), bird_rect_icon.inflate(10,10), 2)
                # Drawing rect is safe
                pygame.draw.rect(SCREEN, (255, 215, 0), bird_rect_icon.inflate(6,6), 3)

        # Show instructions or current selection
        # Just drawing the grid is intuitive enough with selection box.
        
        # Draw Close Button
        draw_close_button()

    # Base
    # Base usually moves unless dead?
    if GAME_STATE != 2: # Stop base on death
        BASE_X_POS -= 1
        if BASE_X_POS <= -SCREEN_WIDTH:
            BASE_X_POS = 0
            
    draw_base()

    pygame.display.update()
    clock.tick(120)
