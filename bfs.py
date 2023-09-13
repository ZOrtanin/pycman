import pygame
import queue

# Определение размеров экрана и клеток
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Pathfinding")

# Определение сетки
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Определение направлений для движения
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Функция для отображения сетки
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK
            elif grid[row][col] == 2:
                color = GREEN
            elif grid[row][col] == 3:
                color = RED
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)

# Функция для выполнения алгоритма BFS
def bfs(start, end):
    
    visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    q = queue.Queue()
    q.put(start)
    visited[start[0]][start[1]] = True

    while not q.empty():
        current = q.get()
        row, col = current

        if current == end:
            print(q)
            return True

        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and not visited[new_row][new_col] and grid[new_row][new_col] != 1:
                q.put((new_row, new_col))
                visited[new_row][new_col] = True
                grid[new_row][new_col] = 3  # Помечаем путь к конечной точке
                pygame.time.delay(100)  # Задержка для визуализации
                draw_grid()
                pygame.display.update()

    
    return False

# Инициализация начальной и конечной точек
start = (0, 0)
end = (GRID_HEIGHT - 1, GRID_WIDTH - 1)

# Генерация препятствий (черных клеток)
for _ in range(GRID_WIDTH * GRID_HEIGHT // 4):
    rand_row = pygame.time.get_ticks() % GRID_HEIGHT
    rand_col = pygame.time.get_ticks() % GRID_WIDTH
    if (rand_row, rand_col) != start and (rand_row, rand_col) != end:
        grid[rand_row][rand_col] = 1

grid[start[0]][start[1]] = 2  # Начальная точка
grid[end[0]][end[1]] = 3  # Конечная точка

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if bfs(start, end):
        break

pygame.quit()