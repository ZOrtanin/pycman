import random
import ast

# карта текстур
with open('level1/game_floor_map.txt', 'r') as file:
    map_textur = ast.literal_eval(file.read())

for row in range(len(map_textur)):
    for col in range(len(map_textur[row])):
        if map_textur[row][col] != 'I' and map_textur[row][col] != 'i':
            map_textur[row][col] = str(random.randint(0,3))

with open('level1/game_floor_map.txt', 'w') as file:
    file.write(str(map_textur))