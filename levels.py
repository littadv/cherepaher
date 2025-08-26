# levels.py — загрузка уровней из текстовых файлов и их обработка
import os
from settings import GRID_SIZE

def load_level(path_to_txt):
    with open(path_to_txt, "r", encoding="utf-8") as f:
        rows = [line.rstrip("\n") for line in f]

    # валидация размера
    if len(rows) != GRID_SIZE or any(len(r) != GRID_SIZE for r in rows):
        raise ValueError(f"Уровень должен быть {GRID_SIZE}x{GRID_SIZE}, а пришло: "
                         f"{len(rows)}x{max(map(len,rows), default=0)}")

    player_pos = None
    star_pos = None
    blocks = []

    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == "T":
                player_pos = [y, x]
            elif ch == "S":
                star_pos = [y, x]
            elif ch == "B":
                blocks.append((y, x))

    if player_pos is None or star_pos is None:
        missing = "черепахи" if player_pos is None else "звезды"
        raise ValueError(f"В уровне нет {missing}")

    return player_pos, star_pos, blocks