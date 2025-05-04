import pgzrun

import pgzero.game
import pgzero.keyboard
from pgzero.actor import Actor
from pgzero.animation import animate
from pgzero.clock import schedule_interval
from pgzero.constants import mouse

import random

keyboard: pgzero.keyboard.keyboard
screen: pgzero.game.screen


cell = Actor("border")
cell1 = Actor("floor")
cell2 = Actor("crack")
cell3 = Actor("bones")


size_w = 9 # ширина поля в клетках
size_h = 10 # высота поля в клетках


WIDTH = size_w * cell.width
HEIGHT = size_h * cell.height

TITLE = "Rougelike"

FPS = 30

mode = "game"
win = 0

my_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0], # [0] * 9
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 2, 1, 3, 1, 1, 0],
    [0, 1, 1, 1, 2, 1, 1, 1, 0],
    [0, 1, 3, 2, 1, 1, 3, 1, 0],
    [0, 1, 1, 1, 1, 3, 1, 1, 0],
    [0, 1, 1, 3, 1, 1, 2, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

char = Actor("stand")
char.top = cell.height
char.left = cell.width
char.health = 100
# char - словарь, где char["health"] = 100 - добавление нового ключа
char.attack = 5

enemies = []
enemy_health = []
enemy_x = []
enemy_y = []
for i in range(5):
    x = random.randint(1, 7) * cell.width
    y = random.randint(1, 7) * cell.height
    enemy = Actor("enemy", topleft=(x, y))
    enemy.health = random.randint(5, 20)
    enemy.attack = random.randint(5, 20)
    enemy.bonus = random.randint(0, 2)
    enemies.append(enemy)
    enemy_health.append(enemy.health)
    enemy_x.append(x)
    enemy_y.append(y)


hearts = []
swords = []


def map_draw():
    # вложенные циклы
    for i in range(len(my_map)): # проход по строкам
        for j in range(len(my_map[0])): # проход по столбцам
            if my_map[i][j] == 0:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()

            elif my_map[i][j] == 1:
                cell1.left = cell1.width * j
                cell1.top = cell1.height * i
                cell1.draw()

            elif my_map[i][j] == 2:
                cell2.left = cell2.width * j
                cell2.top = cell2.height * i
                cell2.draw()

            elif my_map[i][j] == 3:
                cell3.left = cell3.width * j
                cell3.top = cell3.height * i
                cell3.draw()


def draw():
    if mode == "game":
        map_draw()
        char.draw()
        screen.draw.text(f"HP: {str(char.health)}", center=(80, 475), color="green", fontname="segoeprintbold", fontsize=30)
        screen.draw.text(f"AP: {str(char.attack)}", center=(380, 475), color="orange", fontname="segoeprintbold", fontsize=30)

        for i in range(len(enemies)):
            enemies[i].draw()
            screen.draw.text(str(enemy_health[i]), topleft=(enemy_x[i] + 10, enemy_y[i] - 25), color="red", fontname="segoeprintbold", fontsize=15)

        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()

    elif mode == "end":
        screen.fill("#176b78")
        if win == 1:
            screen.draw.text("Победа!", center=(WIDTH/2, HEIGHT/2), color="white", fontname="segoeprintbold", fontsize=30)
        if win == 0:
            screen.draw.text("Поражение!", center=(WIDTH/2, HEIGHT/2), color="white", fontname="segoeprintbold", fontsize=30)



def on_key_down(key):
    old_x = char.x
    old_y = char.y
    if keyboard.right and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = "stand"
    elif keyboard.left and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = "left"
    elif keyboard.up and char.y - cell.height > cell.width:
        char.y -= cell.height
    elif keyboard.down and char.y + cell.height < HEIGHT - cell.width:
        char.y += cell.height

    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        char.health -= enemy.attack
        if enemy.health <= 0:
            if enemy.bonus == 1:
                heart = Actor("heart")
                heart.pos = enemy.pos
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor("sword")
                sword.pos = enemy.pos
                swords.append(sword)
            enemies.pop(enemy_index)

def victory():
    global mode, win
    if enemies == [] and char.health > 0:
        mode = "end"
        win = 1
    elif char.health <= 0:
        mode = "end"
        win = 0



def update(dt):
    victory()
    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break

    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break




pgzrun.go()