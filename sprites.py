# sprites.py — загрузка и масштабирование спрайтов (позволяет использовать спрайты разного размера)
import os
import pygame
from settings import CELL_SIZE

def load_sprites(folder: str) -> dict[str, pygame.Surface]:
    sprites = {}
    for fn in os.listdir(folder):
        if fn.lower().endswith(".png"):
            name = os.path.splitext(fn)[0]
            img = pygame.image.load(os.path.join(folder, fn)).convert_alpha()
            sprites[name] = pygame.transform.smoothscale(img, (CELL_SIZE, CELL_SIZE))
    return sprites