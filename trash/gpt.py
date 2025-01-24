import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 800
screen_height = 600

# Цвета
black = (0, 0, 0)
yellow = (255, 255, 0)
GREEN = (0, 252, 76)
BLUE = (0, 215, 252)
ORENGE = (252, 105, 0)

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pac-Man")

# Радиус пакмана и призрака
pacman_radius = 30
ghost_radius = 30

# Позиция пакмана и призрака
pacman_x = 400
pacman_y = 300
ghost_x = 100
ghost_y = 100

# Позиция стен (прямоугольники)
walls = [
    pygame.Rect(100, 100, 100, 20),
    pygame.Rect(200, 200, 20, 200),
    pygame.Rect(400, 100, 20, 300),
    pygame.Rect(500, 300, 100, 20),
    # Добавьте больше стен здесь
]

# Функция для отображения пакмана (круг)
def draw_pacman(x, y):
    pygame.draw.circle(screen, yellow, (x, y), pacman_radius)

# Функция для отображения призрака (круг)
def draw_ghost(x, y):
    pygame.draw.circle(screen, GREEN, (x, y), ghost_radius)

# Функция для отображения стен (прямоугольников)
def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление пакманом
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= 1
    if keys[pygame.K_RIGHT]:
        pacman_x += 1
    if keys[pygame.K_UP]:
        pacman_y -= 1
    if keys[pygame.K_DOWN]:
        pacman_y += 1

    # Проверка коллизии пакмана со стенами
    pacman_rect = pygame.Rect(pacman_x - pacman_radius, pacman_y - pacman_radius, 2 * pacman_radius, 2 * pacman_radius)
    for wall in walls:
        if pacman_rect.colliderect(wall):
            print('work')
            # Если есть коллизия, вернуть пакмана на предыдущее положение
            pacman_x = pacman_rect.centerx
            pacman_y = pacman_rect.centery

    # Очистка экрана
    screen.fill(black)

    # Отображение стен
    draw_walls()

    # Отображение пакмана и призрака
    draw_pacman(pacman_x, pacman_y)
    draw_ghost(ghost_x, ghost_y)

    # Обновление экрана
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()
sys.exit()