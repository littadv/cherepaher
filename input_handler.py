# input_handler.py — обработка ввода с клавиатуры
import pygame

# клавиша -> (метка спрайта, dy, dx)
DIRS = {
    pygame.K_w: ("W", -1,  0),
    pygame.K_s: ("S",  1,  0),
    pygame.K_a: ("A",  0, -1),
    pygame.K_d: ("D",  0,  1),
}

def handle_input(event):
    if event.type == pygame.KEYDOWN and event.key in DIRS:
        return DIRS[event.key]
    return None