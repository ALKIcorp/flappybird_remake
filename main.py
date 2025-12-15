import pygame
import sys
import os

# Import Modules
from src.config import *
from src.assets import AssetManager
from src.logic import *
from src.ui import *

# Initialize Pygame
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Load Assets
assets = AssetManager()
assets.load_assets()

# Game Variables
game_active = False
score = 0
high_score = 0
game_state = STATE_MENU

# Bird Logic
bird_index = 0
current_bird_color = 0
bird_frames = assets.bird_variants[current_bird_color]
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))
bird_movement = 0

# Pipes
pipe_list = []

# Base
base_x_pos = 0

# Timers
pygame.time.set_timer(BIRDFLAP, 200)
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == STATE_MENU:
                if SETTINGS_BTN_RECT.collidepoint(event.pos):
                    game_state = STATE_SETTINGS
                else:
                    # Start Game
                    game_state = STATE_PLAYING
                    game_active = True
                    bird_movement = 0
                    bird_movement -= 6
                    pipe_list.clear()
                    bird_index = 0
                    bird_surface = bird_frames[bird_index]
                    bird_rect.center = (50, 256)
                    score = 0
            elif game_state == STATE_GAMEOVER:
                # Restart
                game_state = STATE_MENU
                game_active = False
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0
            elif game_state == STATE_SETTINGS:
                # Close button or selection
                if SETTINGS_BTN_RECT.collidepoint(event.pos):
                    game_state = STATE_MENU
                else:
                    # Check Bird Selection
                    start_x = 40
                    start_y = 100
                    padding = 45
                    
                    for i in range(10):
                        row = i // 5
                        col = i % 5
                        x = start_x + (col * padding)
                        y = start_y + (row * padding * 1.5)
                        
                        item_rect = pygame.Rect(0, 0, 40, 40)
                        item_rect.center = (x, y)
                        
                        if item_rect.collidepoint(event.pos):
                            current_bird_color = i
                            bird_frames = assets.bird_variants[current_bird_color]
                            bird_surface = bird_frames[bird_index]
                            game_state = STATE_MENU
                            break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == STATE_MENU:
                    game_state = STATE_PLAYING
                    game_active = True
                    bird_movement = 0
                    bird_movement -= 6
                    pipe_list.clear()
                    bird_index = 0
                    bird_surface = bird_frames[bird_index]
                    bird_rect.center = (50, 256)
                    score = 0
                elif game_state == STATE_PLAYING:
                    bird_movement = 0
                    bird_movement -= 6
                elif game_state == STATE_GAMEOVER:
                    game_state = STATE_MENU
                    game_active = False
                    pipe_list.clear()
                    bird_rect.center = (50, 256)
                    bird_movement = 0
                    score = 0
            
            if event.key == pygame.K_s and game_state == STATE_MENU:
                game_state = STATE_SETTINGS

            if game_state == STATE_SETTINGS:
                if event.key == pygame.K_RIGHT:
                    current_bird_color = (current_bird_color + 1) % 10
                    bird_frames = assets.bird_variants[current_bird_color]
                    bird_surface = bird_frames[bird_index]
                if event.key == pygame.K_LEFT:
                    current_bird_color = (current_bird_color - 1) % 10
                    bird_frames = assets.bird_variants[current_bird_color]
                    bird_surface = bird_frames[bird_index]

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe(assets.pipe_surface))

        if event.type == BIRDFLAP and game_active:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface = bird_frames[bird_index]
            bird_rect = bird_surface.get_rect(center = (50, bird_rect.centery))

    # Background
    SCREEN.blit(assets.bg_surface, (0,0))

    if game_state == STATE_MENU:
        SCREEN.blit(assets.message_surface, assets.message_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
        draw_settings_button(SCREEN)
        
    elif game_state == STATE_PLAYING:
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird_surface, bird_movement)
        bird_rect.centery += bird_movement
        SCREEN.blit(rotated_bird, bird_rect)
        
        if check_collision(pipe_list, bird_rect):
             game_state = STATE_GAMEOVER
             game_active = False

        pipe_list = move_pipes(pipe_list)
        draw_pipes(SCREEN, pipe_list, assets.pipe_surface)
        
        # Pipe Score Check
        # Simplified as previously implemented inline
        # Using module logic need score return?
        # Let's do simple check here or logic?
        # Logic module handles collision, score updating is simple state.
        for pipe in pipe_list:
            if 48 < pipe.centerx < 52:
                score += 0.5 
        
        display_score(SCREEN, score, assets.score_images, 'main_game')
        
    elif game_state == STATE_GAMEOVER:
        draw_pipes(SCREEN, pipe_list, assets.pipe_surface)
        rotated_bird = rotate_bird(bird_surface, bird_movement)
        SCREEN.blit(rotated_bird, bird_rect)
        
        SCREEN.blit(assets.gameover_surface, assets.gameover_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))
        high_score = update_score(score, high_score)
        display_score(SCREEN, score, assets.score_images, 'game_over')

    elif game_state == STATE_SETTINGS:
        draw_settings_menu(SCREEN, assets.bird_variants, current_bird_color)

    # Base
    if game_state != STATE_GAMEOVER:
        base_x_pos -= 1
        if base_x_pos <= -SCREEN_WIDTH:
            base_x_pos = 0
            
    draw_base(SCREEN, assets.base_surface, base_x_pos)

    pygame.display.update()
    clock.tick(120)
