import pygame
from pygame import mixer
import time
import random

WIDTH = 1920
HEIGHT = 1080
FPS = 60
speed = 0.3

width = 20
wall = 12
columns = WIDTH // width - 1
rows = HEIGHT // width - 2

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH + wall, HEIGHT + wall))
pygame.mouse.set_visible(False)
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

grid = []
visited = []
stack = []
solution = {}

move_sound = pygame.mixer.Sound('pew.wav')
truck_sound = pygame.mixer.Sound('truck.wav')

def build_grid(width):
    for i in range(rows):
        x = x00
        y = y00 + i * width
        for j in range(columns):
            pygame.draw.line(screen, BLACK, [x, y], [x + width, y])
            pygame.draw.line(screen, BLACK, [x + width, y], [x + width, y + width])
            pygame.draw.line(screen, BLACK, [x + width, y + width], [x, y + width])
            pygame.draw.line(screen, BLACK, [x, y + width], [x, y])
            grid.append((x, y))
            x = x00 + j * width


def up(x, y):
    pygame.draw.rect(screen, WHITE, (x + wall, y - width + wall, width - wall, width * 2 - wall), 0)
    pygame.display.update()
    move_sound.play()

def down(x, y):
    pygame.draw.rect(screen, WHITE, (x + wall, y + wall, width - wall, width * 2 - wall), 0)
    pygame.display.update()
    move_sound.play()


def left(x, y):
    pygame.draw.rect(screen, WHITE, (x - width + wall, y + wall, width * 2 - wall, width - wall), 0)
    pygame.display.update()
    move_sound.play()


def right(x, y):
    pygame.draw.rect(screen, WHITE, (x + wall, y + wall, width * 2 - wall, width - wall), 0)
    pygame.display.update()
    move_sound.play()


def single_cell(x, y):
    pygame.draw.rect(screen, RED, (x + wall, y + wall, width - wall, width - wall), 0)
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, WHITE, (x + wall, y + wall, width - wall, width - wall), 0)
    pygame.display.update()
    truck_sound.play()


def solution_cell(x0, x, y0, y, color):
    if x == x0 and y < y0:
        pygame.draw.rect(screen, color, (x + wall, y + wall, width - wall, width * 2 - wall), 0)
    if x == x0 and y > y0:
        pygame.draw.rect(screen, color, (x + wall, y - width + wall, width - wall, width * 2 - wall), 0)
    if x > x0 and y == y0:
        pygame.draw.rect(screen, color, (x - width + wall, y + wall, width * 2 - wall, width - wall), 0)
    if x < x0 and y == y0:
        pygame.draw.rect(screen, color, (x + wall, y + wall, width * 2 - wall, width - wall), 0)
    pygame.display.update()


def create_maze(x, y):
    single_cell(x, y)
    stack.append((x, y))
    visited.append((x, y))
    while len(stack) > 0:
        time.sleep(speed)
        cell = []
        if (x + width, y) not in visited and (x + width, y) in grid:
            cell.append("right")
        if (x - width, y) not in visited and (x - width, y) in grid:
            cell.append("left")
        if (x, y + width) not in visited and (x, y + width) in grid:
            cell.append("down")
        if (x, y - width) not in visited and (x, y - width) in grid:
            cell.append("up")
        if len(cell) > 0:
            cell_chosen = (random.choice(cell))
            if cell_chosen == "right":
                right(x, y)
                solution[(x + width, y)] = x, y
                x = x + width
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "left":
                left(x, y)
                solution[(x - width, y)] = x, y
                x = x - width
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "down":
                down(x, y)
                solution[(x, y + width)] = x, y
                y = y + width
                visited.append((x, y))
                stack.append((x, y))
            elif cell_chosen == "up":
                up(x, y)
                solution[(x, y - width)] = x, y
                y = y - width
                visited.append((x, y))
                stack.append((x, y))
            pygame.draw.rect(screen, RED, (x + wall, y + wall, width - wall, width - wall), 0)
            time.sleep(speed)
            pygame.display.update()
        else:
            x, y = stack.pop()
            single_cell(x, y)
            time.sleep(speed)
            backtracking_cell(x, y)


def solve_maze(x, y):
    x0, y0 = solution[x, y]
    solution_cell(x0, WIDTH - width * 2, y0, HEIGHT - width * 2, GREEN)
    pygame.draw.rect(screen, RED, (x00 + wall, y00 + wall, width - wall, width - wall), 0)
    while (x, y) != (x00, y00):
        x, y = solution[x, y]
        x0, y0 = solution[x, y]
        solution_cell(x0, x, y0, y, GREEN)
        pygame.draw.rect(screen, RED, (WIDTH - width * 2 + wall, HEIGHT - width * 2 + wall, width - wall, width - wall),
                         0)
        pygame.display.update()
        time.sleep(speed)
        if (x0, y0) == (x00, y00):
            print(x, y, x0, y0)
            solution_cell(x0, x, y0, y, GREEN)
            break


x00, y00 = width, width
build_grid(width)
create_maze(x00, y00)

time.sleep(1)
solve_maze(WIDTH - width * 2, HEIGHT - width * 2)
pygame.draw.rect(screen, RED, (x00 + wall, y00 + wall, width - wall, width - wall), 0)
pygame.display.update()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
