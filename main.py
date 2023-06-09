import pygame
import random
from tkinter import messagebox


def game(difficulty):
    # Инициализация Pygame
    pygame.init()

    # Определение цветов
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)

    # Определение размеров окна и клеток для каждого уровня сложности
    DIFFICULTY_LEVELS = {
        "легкий": (10, 10, 10),
        "средний": (20, 20, 60),
        "сложный": (25, 25, 80)
    }

    ROWS, COLS, MINE_COUNT = DIFFICULTY_LEVELS[difficulty]

    # Определение размеров окна и клеток
    WINDOW_WIDTH = COLS * 40
    WINDOW_HEIGHT = ROWS * 40
    CELL_SIZE = 40

    # Создание окна
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + 40))
    pygame.display.set_caption("Сапер")

    clock = pygame.time.Clock()

    # Создание сетки
    grid = [[0] * COLS for _ in range(ROWS)]
    revealed = [[False] * COLS for _ in range(ROWS)]
    flags = [[False] * COLS for _ in range(ROWS)]

    # Размещение мин на сетке
    mine_coordinates = random.sample(range(ROWS * COLS), MINE_COUNT)
    for coord in mine_coordinates:
        row = coord // COLS
        col = coord % COLS
        grid[row][col] = -1

    # Вычисление количества мин вокруг каждой клетки
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1:
                count = 0
                for i in range(max(0, row - 1), min(row + 2, ROWS)):
                    for j in range(max(0, col - 1), min(col + 2, COLS)):
                        if grid[i][j] == -1:
                            count += 1
                grid[row][col] = count

    # Переменные для таймера
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    # Основной игровой цикл
    game_over = False
    win = False
    # Счетчик мин
    counter = 0
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not win:
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // CELL_SIZE
                    # Учесть смещение окна игры
                    row = (mouse_pos[1] - 40) // CELL_SIZE

                    if event.button == 1:  # Левая кнопка мыши
                        if not flags[row][col]:
                            if grid[row][col] == -1:
                                game_over = True
                            else:
                                revealed[row][col] = True
                                if grid[row][col] == 0:
                                    # Раскрытие соседних клеток, если текущая клетка пустая
                                    stack = [(row, col)]
                                    while stack:
                                        r, c = stack.pop()
                                        for i in range(max(0, r - 1), min(r + 2, ROWS)):
                                            for j in range(max(0, c - 1), min(c + 2, COLS)):
                                                if not revealed[i][j]:
                                                    revealed[i][j] = True
                                                    if grid[i][j] == 0:
                                                        stack.append((i, j))

                    elif event.button == 3:  # Правая кнопка мыши
                        if not revealed[row][col]:
                            flags[row][col] = not flags[row][col]
                            counter += 1

        # Очистка окна
        window.fill(GRAY)

        # Отображение клеток
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row *
                                   CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)

                if revealed[row][col]:
                    if grid[row][col] == -1:  # Мина
                        pygame.draw.rect(window, RED, rect)
                    else:  # Число
                        pygame.draw.rect(window, WHITE, rect)
                        if grid[row][col] > 0:
                            font = pygame.font.Font(None, 30)
                            text = font.render(
                                str(grid[row][col]), True, BLACK)
                            text_rect = text.get_rect(center=rect.center)
                            window.blit(text, text_rect)
                elif flags[row][col]:  # Флаг
                    pygame.draw.rect(window, WHITE, rect)
                    pygame.draw.line(
                        window, BLACK, rect.topleft, rect.bottomright)
                    pygame.draw.line(
                        window, BLACK, rect.bottomleft, rect.topright)

                pygame.draw.rect(window, BLACK, rect, 1)  # Границы клеток

        # Проверка на победу
        if not game_over:
            revealed_count = sum(sum(row) for row in revealed)
            if revealed_count == ROWS * COLS - MINE_COUNT:
                game_over = True
                win = True

        # Расчет времени и отображение таймера
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = f"Время: {elapsed_time} сек."
        font = pygame.font.Font(None, 30)
        text = font.render(timer_text, True, BLACK)
        window.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    # Отображение сообщения о результате игры
    if win:
        messagebox.showinfo(
            'Победа!', f"Затраченное время {timer_text}, Сложность: {difficulty}")
    else:
        messagebox.showinfo(
            'Проигрыш', f"Осталось мин: {MINE_COUNT-counter}, Сложность: {difficulty}")
    # Завершение Pygame
    pygame.quit()
