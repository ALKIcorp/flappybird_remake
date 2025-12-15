import pygame
import random
from .config import *

def create_pipe(pipe_surface):
    random_pipe_pos = random.choice([200, 300, 400])
    bottom_pipe = pipe_surface.get_rect(midtop = (SCREEN_WIDTH + 50, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (SCREEN_WIDTH + 50, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return [pipe for pipe in pipes if pipe.right > -50]

def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True # Collision

    if bird_rect.top <= -100 or bird_rect.bottom >= FLOOR_HEIGHT:
        return True # Collision

    return False

def rotate_bird(bird_surface, movement):
    new_bird = pygame.transform.rotozoom(bird_surface, -movement * 3, 1)
    return new_bird

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
