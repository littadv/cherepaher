# game.py — основной файл игры
import os, sys, pygame # импорт библиотек
from settings import GRID_SIZE, CELL_SIZE, SIDE, FPS, WINDOW_TITLE, GAME_SIZE # ← импорт настроек
from sprites import load_sprites # ← импорт функции загрузки спрайтов
from levels import load_level # ← импорт функции загрузки уровней
from input_handler import handle_input # ← импорт функции обработки ввода
from main_menu import run_menu, select_level_menu # ← импорт главного меню
from level_gen import save_generate_level   # ← импорт функции генерации уровней    
# пути к ресурсам
BASE = os.path.dirname(__file__)
SPRITES_DIR = os.path.join(BASE, "sprites")
LEVELS_DIR = os.path.join(BASE, "levels")

pygame.init()
screen = pygame.display.set_mode(GAME_SIZE)
pygame.display.set_caption(WINDOW_TITLE)
icon_path = os.path.join(SPRITES_DIR, "icon.png")
if os.path.exists(icon_path):
    pygame.display.set_icon(pygame.image.load(icon_path))

sprites = load_sprites(SPRITES_DIR)
# 
save_generate_level (LEVELS_DIR)  # ← генерация уровней


# Список уровней
level_files = sorted(
    [f for f in os.listdir(LEVELS_DIR) if f.startswith("level_")],
    key=lambda x: int(x.split("_")[1].split(".")[0])
)
current_level = 0

# Главное меню
menu_result = run_menu(screen)
if menu_result == "level_select":
    current_level = select_level_menu(screen, level_files)
elif menu_result == "exit":
    sys.exit()

pygame.display.set_caption(WINDOW_TITLE + "  — Уровень " + str(current_level + 1))
player_pos, star_pos, blocks = load_level(os.path.join(LEVELS_DIR, level_files[current_level]))
turtle_dir = "S"  # начальное направление

clock = pygame.time.Clock()
running = True
win_shown = False

def show_popup(screen, message):
    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, (0, 0, 0), (255, 255, 200))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    pygame.draw.rect(screen, (255, 255, 200), rect.inflate(40, 40))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(1500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        move = handle_input(event)
        if move:
            direction, dy, dx = move
            new_pos = [player_pos[0] + dy, player_pos[1] + dx]
            if (
                0 <= new_pos[0] < GRID_SIZE and
                0 <= new_pos[1] < GRID_SIZE and
                (new_pos[0], new_pos[1]) not in blocks
            ):
                player_pos = new_pos
                turtle_dir = direction

    # Победа
    if player_pos == star_pos and not win_shown:
        show_popup(screen, f"Уровень {current_level + 1} пройден!")
        current_level += 1
        pygame.display.set_caption(WINDOW_TITLE + "  — Уровень " + str(current_level))
        if current_level < len(level_files):
            player_pos, star_pos, blocks = load_level(os.path.join(LEVELS_DIR, level_files[current_level]))
            turtle_dir = "S"
            win_shown = False
        else:
            show_popup(screen, "Все уровни пройдены!")
            running = False
        win_shown = True

    # Отрисовка
    screen.fill((40, 40, 40))
    # Сетка 
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, (80, 80, 80), (i * CELL_SIZE, 0), (i * CELL_SIZE, SIDE), 1)
        pygame.draw.line(screen, (80, 80, 80), (0, i * CELL_SIZE), (SIDE, i * CELL_SIZE), 1)
    # Блоки
    for by, bx in blocks:
        screen.blit(sprites["block"], (bx * CELL_SIZE, by * CELL_SIZE))
    # Звезда
    screen.blit(sprites["star"], (star_pos[1] * CELL_SIZE, star_pos[0] * CELL_SIZE))
    # Черепашка
    turtle_key = f"turtle_{turtle_dir}"
    screen.blit(sprites[turtle_key], (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()