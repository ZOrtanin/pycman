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

class DrawMap(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((420, 540))
        #self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = 30 #x
        self.rect.y = 30 #y

        self.walls = []

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
                    #print(round((pos[1]-37)/15))
                    if game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] == '0':
                        game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] = '1'
                    elif game_fild[round((pos[1]-37)/15)][round((pos[0]-37)/15)] == '1':
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

    def DrawBFS(self,queue,visited,goal,start,graph):
        #print("работа алгоритма")
        #рисуем путь работы алгоритма
        # queue , visited = ghost.logic3()
        path_head,path_segment = goal,goal
        while path_segment and path_segment in visited:
            pygame.draw.rect(self.image, pygame.Color('white'), get_rect(*path_segment), border_radius=TILE//3)
            path_segment = visited[path_segment]
        pygame.draw.rect(self.image, pygame.Color('blue'), get_rect(*start), border_radius=TILE//3)
        pygame.draw.rect(self.image, pygame.Color('magenta'), get_rect(*path_head), border_radius=TILE//3)

    def GetWalls(self):
        walls = []
        for row in range(len(game_fild)):
            for col in range(len(game_fild[row])):
                if game_fild[row][col] == '1':
                    walls.append(pygame.Rect(col*15, row*15, 15, 15))
        # print(walls)
        return walls

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
        self.image.fill(BLACK)
        self.image.set_alpha(200)
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
        y_real = self.rect.y/15-30
        x_real = self.rect.x/15-30
        #print(str(x)+' '+str(y))
        cords = game_fild[y][x]       
        
        sensor_left = game_fild[y][x-1]
        sensor_top = game_fild[y-1][x]

        try: # обрабатываем ощибку отсутствия элемента массива
            sensor_right = game_fild[y][x+1]
            sensor_bottom = game_fild[y+1][x]
        except:
            print('ошибка')
            sensor_right = '0'            
            sensor_bottom = '0'

        
        # Кнопки упровления
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and sensor_left != '1' and x_real.is_integer():     
            self.speed_x = -self.speed
            self.speed_y = 0
        if keystate[pygame.K_RIGHT] and sensor_right != '1' and x_real.is_integer():
            self.speed_x = self.speed
            self.speed_y = 0
        if keystate[pygame.K_UP] and sensor_top != '1' and y_real.is_integer():  
            self.speed_y = -self.speed
            self.speed_x = 0
        if keystate[pygame.K_DOWN] and sensor_bottom != '1' and y_real.is_integer():            
            self.speed_y = self.speed
            self.speed_x = 0

        # столкновения со стенами
        if sensor_left == '1' and self.speed_x < 0 :
            self.speed_x = 0
        if sensor_right == '1' and self.speed_x > 0 :            
            self.speed_x = 0
        if sensor_top == '1' and self.speed_y < 0 :
            self.speed_y = 0            
        if sensor_bottom == '1' and self.speed_y > 0 :            
            self.speed_y = 0   

        # Кушаем еду на карте
        if cords == 'e':
            #print('work')
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
        rect = pygame.Rect(0, 10, 30, 30)
        fill_color = YELLOW
        pygame.draw.circle(self.image, fill_color, (7,7), 7)        
        pygame.draw.rect(window_surface, YELLOW, get_rect(x-1,y), border_radius=15//3)
        #pygame.draw.rect(self.image, fill_color, rect)

class Pycman2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((45, 45))
        #self.image.fill(BLACK)
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()

        cords = get_cord(6,14)
        self.rect.x = cords[0] #x
        self.rect.y = cords[1] #y

        self.speed = 6

        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        comands = []
        x,y = get_my_rect(self.rect.x,self.rect.y)
        print(x,y)
        cords = game_fild[int(y)][int(x)]
        sensor_left = game_fild[y][x-1]
        sensor_top = game_fild[y-1][x]

        try: # обрабатываем ощибку отсутствия элемента массива
            sensor_right = game_fild[y][x+1]
            sensor_bottom = game_fild[y+1][x]
        except:
            print('ошибка')
            sensor_right = '0'            
            sensor_bottom = '0'

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            comands.append('left')
        if keystate[pygame.K_RIGHT]:
            comands.append('right') 
        if keystate[pygame.K_UP]:
            comands.append('top')
        if keystate[pygame.K_DOWN]:
            comands.append('bottom')

            
        x_not = (self.rect.x / 15)-30
        y_not = (self.rect.y / 15)-30
        
        if x_not.is_integer() and y_not.is_integer():
            if comands != [] :                
                if comands[0] == 'left' and sensor_left != '1':
                    self.speed_x = -self.speed
                    self.speed_y = 0
                if comands[0] == 'right' and sensor_right != '1':
                    self.speed_x = self.speed
                    self.speed_y = 0
                if comands[0] == 'top' and sensor_top != '1':
                    self.speed_x = 0
                    self.speed_y = -self.speed
                if comands[0] == 'bottom' and sensor_bottom != '1':
                    self.speed_x = 0
                    self.speed_y = self.speed 

            # столкновения со стенами
            if sensor_left == '1' and self.speed_x < 0 :
                self.speed_x = 0
            if sensor_right == '1' and self.speed_x > 0 :            
                self.speed_x = 0
            if sensor_top == '1' and self.speed_y < 0 :
                self.speed_y = 0            
            if sensor_bottom == '1' and self.speed_y > 0 :            
                self.speed_y = 0  

        # столкновение с краями карты
        if self.rect.right > 15*28+30:
            self.rect.left = 30
        if self.rect.left < 30:
            self.rect.left = 15*28
        

        # Кушаем еду на карте
        if cords == 'e':            
            game_fild[int(y)][int(x)] = '0'
            #eats_count += 1        

    	# движение
        self.rect.x += self.speed_x    
        self.rect.y += self.speed_y          

    	# Рисуем персонажа        
        fill_color = YELLOW
        pygame.draw.circle(self.image, fill_color, (45/2,45/2), 7)        
        
class Pycman3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((15, 15))
        self.image.fill(GREY)
        #self.image.set_alpha(200)
        self.rect = self.image.get_rect()

        cords = get_cord(7,11)
        self.rect.x = cords[0] #x
        self.rect.y = cords[1] #y

        self.speed = 7

        self.speed_x = 0
        self.speed_y = 0
        self.comands = []

    def update(self): 
        
        keystate = pygame.key.get_pressed()

        x,y = get_my_rect(self.rect.centerx,self.rect.centery)
        print(x,y)
        cords = game_fild[int(y)][int(x)]
        print(cords)
        sensor_left = game_fild[y][x-1]
        sensor_top = game_fild[y-1][x]

        try: # обрабатываем ощибку отсутствия элемента массива
            sensor_right = game_fild[y][x+1]
            sensor_bottom = game_fild[y+1][x]
        except:
            print('ошибка')
            sensor_right = '0'            
            sensor_bottom = '0'
        
        if keystate[pygame.K_LEFT]:
            print(sensor_left)
            self.comands.append('left')
        if keystate[pygame.K_RIGHT]:
            self.comands.append('right') 
        if keystate[pygame.K_UP]:
            self.comands.append('top')
        if keystate[pygame.K_DOWN]:
            self.comands.append('bottom')

        if self.comands != []:
            if self.comands[0] == 'left' and sensor_left != '1':
                self.speed_x = -self.speed
                #self.speed_y = 0
            if self.comands[0] == 'right' and sensor_right != '1':
                self.speed_x = self.speed
                #self.speed_y = 0
            if self.comands[0] == 'top' and sensor_top != '1':
                #self.speed_x = 0
                self.speed_y = -self.speed
            if self.comands[0] == 'bottom' and sensor_bottom != '1':
                #self.speed_x = 0
                self.speed_y = self.speed 
        
        if self.comands != []:
            self.comands.pop(0)
        
            

        walls = level.GetWalls()
        pacman_rect = pygame.Rect(self.rect.x - 30, self.rect.y - 30,  15,  15)
        flag = False

        crash_walls = []

        for wall in walls:
            if pacman_rect.colliderect(wall):
                # Если есть коллизия, вернуть пакмана на предыдущее положение
                flag = True
                print(wall.centerx)
                print(self.rect.centerx)
                crash_walls.append(wall)        

        min_distance = float('inf')
        crash_wall = None

        for wall_my in crash_walls:
            distance = GetDistance((self.rect.centerx,self.rect.centery), (wall_my.centerx,wall_my.centery))
            if distance < min_distance:
                #print('work')
                min_distance = distance
                crash_wall = wall_my
        
        horizont = False
        vertical = False
        
        if flag:
            dx = self.rect.centerx - (crash_wall.centerx + 30)
            dy = self.rect.centery - (crash_wall.centery + 30)

            # Проверка стороны пересечения
            if abs(dx) > abs(dy):
                horizont = True
                if dx > 0:
                    # Пересечение справа от стены                    
                    print("Пересечение слева от стены")
                    self.speed_x = 3
                else:
                    # Пересечение слева от стены
                    print("Пересечение справа от стены")
                    self.speed_x = -3
            else:
                vertical = True
                if dy > 0:
                    # Пересечение снизу от стены
                    print("Пересечение сверху от стены")
                    self.speed_y = 3
                else:
                    # Пересечение сверху от стены
                    print("Пересечение снизу от стены")
                    self.speed_y = -3


            # self.rect.x = self.rect.centerx
            # self.rect.y = self.rect.centery
        
        # движение
        self.rect.x += self.speed_x    
        self.rect.y += self.speed_y 

        if flag:    
            print('есть пересичение')
            if vertical:
                print('|||||')
                self.speed_y = 0
            if horizont:
                print('-----')
                self.speed_x = 0 

        # Рисуем персонажа        
        fill_color = YELLOW
        pygame.draw.circle(self.image, fill_color, (7,7), 7)        

def get_my_rect(x,y):
    return int((x-30)/TILE), int((y-30)/TILE)

def get_cord(x,y):
    return (x * TILE) + 15, (y * TILE) + 15

def get_rect(x,y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2 

# Определяем дистанцию
def GetDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Основной цыкл игры    
def main():  
    global is_running,game_fild,player,level 

    play_game = False

    with open('game_fild.txt', 'r') as file:
        game_fild = ast.literal_eval(file.read())

    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()

    # Добовляем поле
    level = DrawMap()
    all_sprites.add(level)

    # Добовляем персонажа на поле
    player = Pycman3()
    all_sprites.add(player)

    # Добовляем персонажа на поле
    # ghost = Ghost()
    # all_sprites.add(ghost)


    # настройки для поиска пути
    start = (14,15)
    goal = start
    queue = deque([start])
    visited = {start:None}
    cur_node = start
      
    
    while is_running:
        time_delta = clock.tick(30)/500.0

        

        # Обработка событий в игре
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False


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