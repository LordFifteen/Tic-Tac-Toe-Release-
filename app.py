import pygame
import sys

pygame.init()
W, H = 450, 550  # Увеличить размер окна
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Крестики-нолики')

# Цвета
BG = (149, 164, 236)
LINE = (115, 125, 172)
X_COLOR = (66, 66, 66)
O_COLOR = (239, 231, 200)
TEXT_COLOR = (255, 255, 255)

board = [[0] * 3 for _ in range(3)]
player = 1  # 1 - X, 2 - O
game_over = False
winner = 0
font = pygame.font.SysFont('Arial', 32)  # Увеличить шрифт
small_font = pygame.font.SysFont('Arial', 24)  # Добавить меньший шрифт

CELL_SIZE = 150  # Размер клетки (450 / 3 = 150)
BOARD_HEIGHT = CELL_SIZE * 3  # Высота игрового поля


def draw_board():
    screen.fill(BG)
    # Линии поля
    for i in range(1, 3):
        pygame.draw.line(screen, LINE, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_HEIGHT), 15)  # Увеличить толщину линий
        pygame.draw.line(screen, LINE, (0, i * CELL_SIZE), (W, i * CELL_SIZE), 15)

    # Фигуры
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:  # X
                offset = 30  # Отступ от краев
                pygame.draw.line(screen, X_COLOR,
                                 (col * CELL_SIZE + offset, row * CELL_SIZE + offset),
                                 ((col + 1) * CELL_SIZE - offset, (row + 1) * CELL_SIZE - offset),
                                 20)  # Увеличить толщину
                pygame.draw.line(screen, X_COLOR,
                                 ((col + 1) * CELL_SIZE - offset, row * CELL_SIZE + offset),
                                 (col * CELL_SIZE + offset, (row + 1) * CELL_SIZE - offset), 20)
            elif board[row][col] == 2:  # O
                pygame.draw.circle(screen, O_COLOR,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 3, 20)  # Увеличить радиус и толщину


def draw_status():
    # Область статуса
    pygame.draw.rect(screen, (40, 40, 40), (0, BOARD_HEIGHT, W, H - BOARD_HEIGHT))

    if game_over:
        if winner == 0:
            text = font.render("Ничья!", True, TEXT_COLOR)
        else:
            text = font.render(f"Победили: {'Крестики' if winner == 1 else 'Нолики'}!", True, TEXT_COLOR)
    else:
        text = font.render(f"Ход: {'Крестики' if player == 1 else 'Нолики'}", True, TEXT_COLOR)

    screen.blit(text, (W // 2 - text.get_width() // 2, BOARD_HEIGHT + 20))

    # Подсказка перезапуска
    restart_text = small_font.render("R - перезапуск", True, (200, 200, 200))
    screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, BOARD_HEIGHT + 60))


def check_win():
    # Проверка строк и столбцов
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    # Диагонали
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            if y < BOARD_HEIGHT:  # Клик в игровом поле
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == 0:
                    board[row][col] = player
                    winner = check_win()
                    if winner:
                        game_over = True
                    elif all(board[i][j] != 0 for i in range(3) for j in range(3)):
                        game_over = True
                        winner = 0
                    else:
                        player = 3 - player  # Смена игрока (1->2, 2->1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Перезапуск
                board = [[0] * 3 for _ in range(3)]
                player = 1
                game_over = False
                winner = 0

    draw_board()
    draw_status()
    pygame.display.update()
