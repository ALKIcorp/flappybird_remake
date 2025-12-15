import pygame
import os
import sys
from PIL import Image
from .config import *

class AssetManager:
    def __init__(self):
        self.base_surface = None
        self.bg_surface = None
        self.pipe_surface = None
        self.gameover_surface = None
        self.message_surface = None
        self.score_images = {}
        self.bird_variants = []
        
    def load_assets(self):
        self.bg_surface = self.load_asset('background-day.png')
        self.base_surface = self.load_asset('base.png')
        self.pipe_surface = self.load_asset_alpha('pipe.png')
        self.gameover_surface = self.load_asset_alpha('gameover.png')
        self.message_surface = self.load_asset_alpha('message.png')
        
        # Load Score Images
        for i in range(10):
            self.score_images[str(i)] = self.load_asset_alpha(f'{i}.png')
            
        # Create Birds
        self.bird_variants = self.create_bird_variants()

    def load_asset(self, name):
        path = os.path.join('assets', name)
        if not os.path.exists(path):
            print(f"Error: Could not find asset {path}")
            sys.exit()
        
        pil_image = Image.open(path).convert('RGBA')
        image_data = pil_image.tobytes()
        image_size = pil_image.size
        
        # Convert means we need display init. Assuming main does it before this.
        return pygame.image.fromstring(image_data, image_size, 'RGBA').convert()

    def load_asset_alpha(self, name, return_pil=False):
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

    def hue_shift_image(self, pil_image, hue_shift):
        r, g, b, a = pil_image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        hsv_image = rgb_image.convert('HSV')
        
        h, s, v = hsv_image.split()
        np_h = h.point(lambda i: (i + int(hue_shift * 255)) % 255)
        
        hsv_image = Image.merge('HSV', (np_h, s, v))
        rgb_shifted = hsv_image.convert('RGB')
        
        r_new, g_new, b_new = rgb_shifted.split()
        return Image.merge('RGBA', (r_new, g_new, b_new, a))

    def create_bird_variants(self):
        base_names = ['bird-down.png', 'bird-mid.png', 'bird-up.png']
        base_images = [self.load_asset_alpha(name, return_pil=True) for name in base_names]
        
        variants = []
        for i in range(10):
            shift = i / 10.0
            colored_frames = []
            for img in base_images:
                new_img = self.hue_shift_image(img, shift)
                raw_str = new_img.tobytes()
                raw_size = new_img.size
                surface = pygame.image.fromstring(raw_str, raw_size, 'RGBA').convert_alpha()
                colored_frames.append(surface)
            variants.append(colored_frames)
        return variants
