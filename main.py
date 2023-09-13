import pygame
from pygame.locals import *
import pygame_gui
import sys
import ast
import random
from collections import deque

pygame.init()
pygame.mixer.init()

pygame.font.init()

pygame.display.set_caption('pycMAN')
window_surface = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 275), (200, 50)),
                                             text='Зпустить игру',
                                             manager=manager)

exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 325), (200, 50)),
                                             text='Выход',
                                             manager=manager)

save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 375), (200, 50)),
                                             text='Сохранить карту',
                                             manager=manager)

load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 425), (200, 50)),
                                             text='Загрузить карту',
                                             manager=manager)

load_eats = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((525, 475), (200, 50)),
                                             text='Загрузить еду',
                                             manager=manager)


clock = pygame.time.Clock()
is_running = True


BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPUR = (249,5,254)
GREY = (33,33,33)


eats_count = 0

f1 = pygame.font.Font(None, 36)

cols, rows = 28, 36

TILE = 15

# Создаем поле игры
game_fild = [ ['0' for r in range(28)] for r in range(36) ]
#print(game_fild)

direction = 'left'

class DrawMap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((420, 540))
        #self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 30 #x
        self.rect.y = 30 #y

    def update(self):

        bg = pygame.Rect(0, 0, 420, 540)
        pygame.draw.rect(self.image, BLACK, bg)


        # Редактор карты
        keystate = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()        

        if pos[0] >= 30 and pos[1] >= 30:
            if pos[0] <= 450 and pos[1] <= 570:
                if keystate[0]:

                    print(round((pos[0]-37)/15))
                    print(round((pos[1]-37)/15))
                    if game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] == '0':
                        game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] = 'e'
                    elif game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] == 'e':
                        game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] = '0'

        

        # Рисуем сетку
        for row in range(len(game_fild)):
            for col in range(len(game_fild[row])):             

                rect = pygame.Rect(col*15, row*15, 15, 15)
                #rect = pygame.Rect(col*15, row*15, 5, 5)
                border_color = GREY
                if game_fild[row][col] == '0':
                    pygame.draw.rect(self.image, border_color, rect, 1)
                if game_fild[row][col] == '1':
                    pygame.draw.rect(self.image, PURPUR, rect)
                if game_fild[row][col] == 'e':
                    #pygame.draw.rect(self.image, YELLOW, rect)
                    pygame.draw.circle(self.image, YELLOW, (col*15+7, row*15+7), 3)

class Pycman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0

        # self.x_start_pos = 240
        # self.y_start_pos = 480
        self.x_start_pos = 15*14+7
        self.y_start_pos = 15*30+30

        self.image = pygame.Surface((15, 15))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x_start_pos #x
        self.rect.bottom = self.y_start_pos #y

        self.speed = 15

        self.speed_x = 0
        self.speed_y = 0

    def update(self): 
        global eats_count       

        # кординаты и сенсоры
        y = int(self.rect.y/15-30)+28
        x = int(self.rect.x/15-30)+28

        cords = game_fild[y][x]       
        
        sensor_left = game_fild[y][x-1]
        sensor_top = game_fild[y-1][x]

        try: # обрабатываем ощибку отсутствия элемента массива
            sensor_right = game_fild[y][x+1]
            sensor_bottom = game_fild[y+1][x]
        except:
            sensor_right = '0'            
            sensor_bottom = '0'

        
        # Кнопки упровления
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and sensor_left != '1':     
            self.speed_x = -self.speed
            self.speed_y = 0
        if keystate[pygame.K_RIGHT] and sensor_right != '1':
            self.speed_x = self.speed
            self.speed_y = 0
        if keystate[pygame.K_UP] and sensor_top != '1':  
            self.speed_y = -self.speed
            self.speed_x = 0
        if keystate[pygame.K_DOWN] and sensor_bottom != '1':            
            self.speed_y = self.speed
            self.speed_x = 0

        # столкновения со стенами
        if sensor_left == '1' and self.speed_x < 0:
            self.speed_x = 0
        if sensor_right == '1' and self.speed_x > 0:            
            self.speed_x = 0
        if sensor_top == '1' and self.speed_y < 0:
            self.speed_y = 0            
        if sensor_bottom == '1' and self.speed_y > 0:            
            self.speed_y = 0   

        # Кушаем еду на карте
        if cords == 'e':
            print('work')
            game_fild[y][x] = '0'
            eats_count += 1      

        # движение
        self.rect.x += self.speed_x    
        self.rect.y += self.speed_y

        # столкновение с краями карты
        if self.rect.right > 15*28+30:
            self.rect.left = 30
        if self.rect.left < 30:
            self.rect.left = 15*27+30
        if self.rect.bottom > 15*36+30:
            self.rect.top = 30
        if self.rect.top < 30:
            self.rect.top = 15*35+30        

    	# Рисуем персонажа
        rect = pygame.Rect(4, 0, 15, 15)
        fill_color = YELLOW
        pygame.draw.circle(self.image, fill_color, (7,7), 7)

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0

        self.x_start_pos = 15*12+7
        self.y_start_pos = 15*15+30

        self.image = pygame.Surface((15, 15))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x_start_pos #x
        self.rect.bottom = self.y_start_pos #y

        self.speed = 15

        self.speed_x = 0
        self.speed_y = 0


    def update(self):
        global direction

        # кординаты и сенсоры
        y = int(self.rect.y/15-30)+28
        x = int(self.rect.x/15-30)+28

        cords = game_fild[y][x]       
        
        sensor_left = game_fild[y][x-1]
        sensor_top = game_fild[y-1][x]

        try: # обрабатываем ощибку отсутствия элемента массива
            sensor_right = game_fild[y][x+1]
            sensor_bottom = game_fild[y+1][x]
        except:
            sensor_right = '0'            
            sensor_bottom = '0'

        # Логика поведения 
        
        choice = []

        if sensor_top != '1' and self.speed_x == 0 and self.speed_y == 0:  
            choice.append('top')

        if sensor_left != '1' and self.speed_x == 0 and self.speed_y == 0:     
            choice.append('left')

        if sensor_bottom != '1' and self.speed_x == 0 and self.speed_y == 0:            
            choice.append('bottom')

        if sensor_right != '1' and self.speed_x == 0 and self.speed_y == 0:
            choice.append('right')

        # Следим за пакманом
        print(player.rect.centerx)
        print(player.rect.bottom)

        if player.rect.bottom < self.rect.bottom :  
            choice.append('top')

        if player.rect.centerx < self.rect.centerx :     
            choice.append('left')

        if player.rect.bottom > self.rect.bottom :            
            choice.append('bottom')

        if player.rect.centerx > self.rect.centerx :
            choice.append('right')

        #print(len(choice))
        direction = choice[random.randint(0, len(choice)-1)]

        if direction == 'left':
            self.speed_x = -self.speed
            self.speed_y = 0
        if direction == 'right':
            self.speed_x = self.speed
            self.speed_y = 0
        if direction == 'top':
            self.speed_x = 0
            self.speed_y = -self.speed
        if direction == 'bottom':
            self.speed_x = 0
            self.speed_y = self.speed

        # столкновения со стенами
        if sensor_left == '1' and self.speed_x < 0:
            self.speed_x = 0
        if sensor_right == '1' and self.speed_x > 0:            
            self.speed_x = 0
        if sensor_top == '1' and self.speed_y < 0:
            self.speed_y = 0            
        if sensor_bottom == '1' and self.speed_y > 0:            
            self.speed_y = 0   

           

        # движение
        # self.rect.x += self.speed_x    
        # self.rect.y += self.speed_y

        # столкновение с краями карты
        if self.rect.right > 15*28+30:
            self.rect.left = 30
        if self.rect.left < 30:
            self.rect.left = 15*27+30
        if self.rect.bottom > 15*36+30:
            self.rect.top = 30
        if self.rect.top < 30:
            self.rect.top = 15*35+30        

        # Рисуем персонажа
        rect = pygame.Rect(4, 0, 15, 15)
        fill_color = RED
        pygame.draw.circle(self.image, fill_color, (7,7), 7)


def get_rect(x,y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2 

def get_next_nodes(x, y):
    check_next_node = lambda x,y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1,0], [0,-1], [1,0], [0,1]
    return [(x+dx,y+dy) for dx,dy in ways if check_next_node(x+dx,y+dy)]

def bfs(start, goal, graph) :
    queue = deque ([start])
    visited = {start: None}

    while queue:
        
        cur_node = queue.popleft()
        
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]

        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node

    return queue,visited

# Основной цыкл игры    
def main():  
    global is_running,game_fild,player 

    play_game = False

    with open('game_fild.txt', 'r') as file:
        game_fild = ast.literal_eval(file.read())

    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    # Добовляем поле
    level = DrawMap()
    all_sprites.add(level)

    # Добовляем персонажа на поле
    player = Pycman()
    all_sprites.add(player)

    # Добовляем персонажа на поле
    ghost = Ghost()
    all_sprites.add(ghost)


    # настройки для поиска пути
    start = (14,15)
    goal = start
    queue = deque([start])
    visited = {start:None}
    cur_node = start
      
    
    while is_running:
        time_delta = clock.tick(10)/500.0

        

        # Обработка событий в игре
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    print('Hello World!')
                    play_game=True

                if event.ui_element == exit_button:
                    print('Good bay!')
                    pygame.quit()
                    sys.exit()

                if event.ui_element == save_button:
                    #print(game_fild)
                    with open('game_fild.txt', 'w') as file:
                        file.write(str(game_fild))

                if event.ui_element == load_button:
                    print('123')
                    with open('game_fild.txt', 'r') as file:
                        game_fild = ast.literal_eval(file.read())
                    print(game_fild)

                if event.ui_element == load_eats:

                    for row in range(len(game_fild)):
                        for col in range(len(game_fild[row])): 
                            if game_fild[row][col] == '0':
                                game_fild[row][col] = 'e'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_game=False

            manager.process_events(event)
          

        
    
        # Обновление
        all_sprites.update()
        window_surface.blit(background, (0, 0))
        
        # рисуем работу алгоритма
        [pygame.draw.rect(window_surface, pygame.Color('forestgreen'),get_rect(x,y)) for x,y in visited]
        [pygame.draw.rect(window_surface, pygame.Color('darkslategray'),get_rect(x,y)) for x,y in queue]

        # bfs, get path to mouse click
        # mouse_pos = get_click_mouse_pos()
        # if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
        #     queue, visited = bfs(start, mouse_pos, graph)
        #     goal = mouse_pos

        # рисуем путь работы алгоритма
        path_head,path_segment = goal,goal
        while path_segment and path_segment in visited:
            pygame.draw.rect(window_surface, pygame.Color('white'), get_rect(*path_segment), border_radius=TILE//3)
            path_segment = visited[path_segment]
        pygame.draw.rect(window_surface, pygame.Color('blue'), get_rect(*start), border_radius=TILE//3)
        pygame.draw.rect(window_surface, pygame.Color('magenta'), get_rect(*path_head), border_radius=TILE//3)

        # # Рисуем сетку
        # for row in range(len(game_fild)):
        # 	for col in range(len(game_fild[row])):

        # 		rect = pygame.Rect(30+col*15, 30+row*15, 15, 15)
        # 		border_color = GREY
        # 		pygame.draw.rect(window_surface, border_color, rect, 1)
        
        all_sprites.draw(window_surface)
        
        if not play_game :
            manager.draw_ui(window_surface)


        manager.update(time_delta)

        # Добовляем текст
        text1 = f1.render(str(eats_count), True,
                  (180, 0, 0))
        window_surface.blit(text1, (550, 50))

        pygame.display.update()


if __name__ == '__main__':
    main()