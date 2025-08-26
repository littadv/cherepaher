# level_gen.py — генерация уровней и сохранение их в текстовые файлы
import os
import random
from settings import GRID_SIZE

def generate_level():
    n = 10
    H = W = 2 * n + 1
    g = [['B'] * W for _ in range(H)]
    far = (1, 1)

    def carve(y, x):
        nonlocal far
        g[y][x] = '.'
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        dead_end = True
        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if 1 <= ny < H - 1 and 1 <= nx < W - 1 and g[ny][nx] == 'B':
                g[y + dy // 2][x + dx // 2] = '.'
                carve(ny, nx)
                dead_end = False
        if dead_end:
            far = (y, x)

    carve(1, 1)
    sy, sx = 1, 1
    ey, ex = far
    g[sy][sx] = 'T'
    g[ey][ex] = 'S'
    trimmed = [row[:GRID_SIZE] for row in g[:GRID_SIZE]]
    return ["".join(row) for row in trimmed]

def save_generate_level(levels_dir):
    os.makedirs(levels_dir, exist_ok=True)
    for i in range(1, 11):   # 10 уровней
        level = generate_level()                  # ← вызов генератора
        fname = os.path.join(levels_dir, f"level_{i}.txt")
        with open(fname, "w", encoding="utf-8") as f:
            # level может быть строкой или списком строк
            if isinstance(level, list):
                f.write("\n".join(level))
            else:
                f.write(str(level))