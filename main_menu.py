# main_menu.py — меню-заглушка (исправлено)
import pygame

def run_menu(screen, title: str = "Cherepaher") -> str:
    font = pygame.font.SysFont(None, 56)
    small = pygame.font.SysFont(None, 28)
    pygame.display.set_caption(title)

    def draw():
        screen.fill((230, 230, 230))
        e = font.render("Нажми Enter чтобы начать", True, (20, 20, 20))
        l = font.render("Нажмите L для выбора уровня", True, (20, 20, 20))
        c = small.render("Esc — выход", True, (80, 80, 80))
        total = e.get_height() + l.get_height() + c.get_height() + 30
        cx, cy = screen.get_width() // 2, screen.get_height() // 2
        y = cy - total // 2
        screen.blit(e, e.get_rect(center=(cx, y + e.get_height() // 2))); y += e.get_height() + 15
        screen.blit(l, l.get_rect(center=(cx, y + l.get_height() // 2))); y += l.get_height() + 15
        screen.blit(c, c.get_rect(center=(cx, y + c.get_height() // 2)))
        pygame.display.flip()

    while True:
        draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "exit"
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): return "start"
                if e.key in (pygame.K_l, pygame.K_l):         return "level_select"
                if e.key == pygame.K_ESCAPE:                   return "exit"

def select_level_menu(screen, level_files):
    font = pygame.font.SysFont(None, 48)
    selected = 0
    while True:
        screen.fill((30, 30, 30))
        title = font.render("Выберите уровень", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 40)))
        rects = []
        for i, _ in enumerate(level_files):
            color = (255, 215, 0) if i == selected else (200, 200, 200)
            text = font.render(f"Уровень {i+1}", True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, 120 + i * 60))
            screen.blit(text, rect); rects.append(rect)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:        return None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:     selected = (selected - 1) % len(level_files)
                elif e.key == pygame.K_DOWN: selected = (selected + 1) % len(level_files)
                elif e.key in (pygame.K_RETURN, pygame.K_SPACE): return selected
                elif e.key == pygame.K_ESCAPE:                   return 0
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, r in enumerate(rects):
                    if r.collidepoint(e.pos): return i


