import numpy as np
from pprint import pprint


def my_print(array):
    print("Красивый вывод массива:")
    for row in array:
        for item in row:
            item = int(item)
            print(f"{item:2d}", end=" ")  # Здесь ":2d" означает выравнивание по ширине в 2 символа
        print()  # Перейти на следующую строку после каждой строки массива

# Размеры массива
width, height = 11, 11

# Создайте двумерный массив для хранения уровней света
light_map = np.zeros((width, height))
my_light_map = [[0 for r in range(height)] for r in range(width) ]
my_map = [[0 for r in range(height)] for r in range(width) ]
shadow_map = [[200 for r in range(height)] for r in range(width) ]

# Установите начальное положение источника света
light_source_x, light_source_y = 5, 5
light_map[light_source_x][light_source_y] = 255  # Максимальный уровень света в источнике

my_light_map[light_source_x][light_source_y] = 255

# Коэффициент затухания
attenuation = 1

# Количество шагов (проходов) распространения света
num_steps = 7

# Распространение света
# for step in range(num_steps):
#     for x in range(1, width - 1):
#         for y in range(1, height - 1):
#             # print(x,y-1)
#             #light_map[x][y] = light_map[x][y] + attenuation * (light_map[x - 1][y] + light_map[x + 1][y] + light_map[x][y - 1] + light_map[x][y + 1])
#             light_map[x][y] = light_map[x][y] + light_map[x - 1][y] + light_map[x + 1][y] + light_map[x][y - 1] + light_map[x][y + 1]
#             light_map[x][y] = light_map[x][y] / 5
#             light_map[x][y] =int(light_map[x][y])
#             #light_map[x][y] = str(light_map[x][y])[3]
#             try:
#                 my_map[x][y] = int(str(light_map[x][y])[-1])
#             except:
#                 pass
                #print('xz')

for step in range(num_steps):
    for x in range(len(light_map)):
        for y in range(len(light_map[x])):
            point1 = my_light_map[x - 1][y]                 
            point2 = my_light_map[x][y - 1]

            try:
                point3 = my_light_map[x + 1][y] 
                point4 = my_light_map[x][y + 1]
            except:
                point3 = 0 
                point4 = 0

            my_light_map[x][y] = my_light_map[x][y] + (point1 + point2 + point3 + point4)*attenuation
            my_light_map[x][y] = my_light_map[x][y] / 5
            my_map[x][y] = my_light_map[x][y]


for x in range(1, width - 1):
    for y in range(1, height - 1):
        try:
            if my_map[x][y] != 0:
                shadow_map[x][y] = int(shadow_map[x][y] / my_map[x][y]) - 33
            if shadow_map[x][y] < 0:
                shadow_map[x][y] = 0
            if shadow_map[x][y] > 200:
                shadow_map[x][y] = 200
        except:
            pass

# Вывод уровней света
#print(light_map)
# my_print(my_map)
my_print(shadow_map)
my_print(my_light_map)


def GetLight(cord):
    global shadow_map

    # Размеры массива
    width, height = 36, 28

    my_map = [[0 for r in range(height)] for r in range(width) ]
    shadow_map_my = [[200 for r in range(height)] for r in range(width) ]
    my_light_map = [[0 for r in range(height)] for r in range(width) ]

    light_source_x, light_source_y = cord
    my_light_map[light_source_x][light_source_y] = 255

    # Коэффициент затухания
    attenuation = 1

    # Количество шагов (проходов) распространения света
    num_steps = 7

    for step in range(num_steps):
        for x in range(len(my_light_map)):
            for y in range(len(my_light_map[x])):
                if game_fild[x - 1][y] != '1':
                    point1 = my_light_map[x - 1][y]
                else:
                    point1 = 0

                if game_fild[x][y - 1] != '1':
                    point2 = my_light_map[x][y - 1]
                else:
                    point2 = 0                   
                

                try:
                    point3 = my_light_map[x + 1][y] 
                    point4 = my_light_map[x][y + 1]
                except:
                    point3 = 0 
                    point4 = 0

                my_light_map[x][y] = my_light_map[x][y] + (point1 + point2 + point3 + point4)*attenuation
                my_light_map[x][y] = my_light_map[x][y] / 5
                my_map[x][y] = my_light_map[x][y]


    for x in range(1, width - 1):
        for y in range(1, height - 1):
            try:
                if my_map[x][y] != 0:
                    shadow_map_my[x][y] = int(shadow_map_my[x][y] / my_map[x][y]) - 33
                if shadow_map_my[x][y] < 0:
                    shadow_map_my[x][y] = 0
                if shadow_map_my[x][y] > 200:
                    shadow_map_my[x][y] = 200
            except:
                pass

    shadow_map = shadow_map_my

# for x in range(1, width + 1):
#     print(x-1)