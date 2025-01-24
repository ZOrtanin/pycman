import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = 800, 600

# Создание окна
window_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Обрезка изображения")

# Определение класса спрайта
class TexturedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, texture):
        super().__init__()
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        


def main():

    # Загрузка текстур
    texture1 = pygame.image.load("assets/trash/player_bottom.png")
    texture1 = pygame.transform.scale(texture1, (50, 50))

    texture2 = pygame.image.load("assets/trash/floor_1.png")
    texture2 = pygame.transform.scale(texture2, (50, 50))

    # Создание спрайтов с текстурами
    sprite1 = TexturedSprite(200, 200, texture1)
    sprite2 = TexturedSprite(200, 200, texture2)


    # Создаем группу для спрайтов
    all_sprites = pygame.sprite.Group()

    # Добавление спрайтов в группу
    all_sprites.add(sprite2, sprite1)

    # player = Pycman()
    # all_sprites.add(player)

    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отрисуем и обновим группу спрайтов
        all_sprites.draw(window_surface)
        all_sprites.update()

        # Обновление экрана
        pygame.display.flip()


if __name__ == '__main__':
    main()