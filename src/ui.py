import pygame
import math
from .config import *

SETTINGS_BTN_RECT = pygame.Rect(SCREEN_WIDTH - 40, 10, 28, 28)
SETTINGS_ANGLE = 0

def draw_base(screen, base_surface, base_x_pos):
    screen.blit(base_surface, (base_x_pos, FLOOR_HEIGHT))
    screen.blit(base_surface, (base_x_pos + SCREEN_WIDTH, FLOOR_HEIGHT))

def draw_pipes(screen, pipes, pipe_surface):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def display_score(screen, score, score_images, game_state_str):
    score_digits = [int(x) for x in list(str(int(score)))]
    total_width = 0
    for digit in score_digits:
        total_width += score_images[str(digit)].get_width()
    
    X_OFFSET = (SCREEN_WIDTH - total_width) / 2
    y_pos = 50
    
    for digit in score_digits:
        screen.blit(score_images[str(digit)], (X_OFFSET, y_pos))
        X_OFFSET += score_images[str(digit)].get_width()

def draw_settings_button(screen):
    global SETTINGS_ANGLE
    rect = SETTINGS_BTN_RECT
    center_x, center_y = rect.centerx, rect.centery
    color = COLOR_WHITE
    hole_color = COLOR_SKY_BLUE
    
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
    base_angles = [0, 60, 120]
    
    for base_a in base_angles:
        rad = math.radians(base_a + SETTINGS_ANGLE)
        offset_dist = (bar_len / 2) - (bar_thickness / 2)
        dx = math.cos(rad) * offset_dist
        dy = math.sin(rad) * offset_dist
        
        p1 = (center_x - dx, center_y - dy)
        p2 = (center_x + dx, center_y + dy)
        
        pygame.draw.line(screen, color, p1, p2, bar_thickness)
        pygame.draw.circle(screen, color, p1, bar_thickness // 2)
        pygame.draw.circle(screen, color, p2, bar_thickness // 2)

    pygame.draw.circle(screen, color, (center_x, center_y), fill_radius)
    pygame.draw.circle(screen, hole_color, (center_x, center_y), hole_radius)

def draw_close_button(screen):
    rect = SETTINGS_BTN_RECT
    color = COLOR_WHITE
    width = 4
    inset = 6
    start_pos1 = (rect.left + inset, rect.top + inset)
    end_pos1 = (rect.right - inset, rect.bottom - inset)
    start_pos2 = (rect.right - inset, rect.top + inset)
    end_pos2 = (rect.left + inset, rect.bottom - inset)
    
    pygame.draw.line(screen, color, start_pos1, end_pos1, width)
    pygame.draw.line(screen, color, start_pos2, end_pos2, width)

def draw_settings_menu(screen, bird_variants, current_color_idx):
    # Draw all 10 birds in a grid
    start_x = 40
    start_y = 100
    padding = 45
    
    for i in range(10):
        row = i // 5
        col = i % 5
        x = start_x + (col * padding)
        y = start_y + (row * padding * 1.5)
        
        bird_icon = bird_variants[i][1] # Midflap
        bird_rect_icon = bird_icon.get_rect(center=(x,y))
        screen.blit(bird_icon, bird_rect_icon)
        
        if i == current_color_idx:
            pygame.draw.rect(screen, (255, 215, 0), bird_rect_icon.inflate(6,6), 3)

    draw_close_button(screen)
