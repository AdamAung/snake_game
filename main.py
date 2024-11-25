import pygame, sys
from pygame.math import Vector2
import random


class Snake:
    def __init__(self):
        self.body = [Vector2(2, 10), Vector2(3, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * 10)
            y_pos = int(block.y * 10)
            block_rect = pygame.Rect(x_pos, y_pos, 10, 10)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        self.body.insert(0, self.body[0] + self.direction)
        # remove the last element of the body array
        self.body.pop()


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number)
        self.y = random.randint(0, cell_number)
        self.fruit_pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.fruit_pos.x * 10), int(self.fruit_pos.y * 10), 10, 10)
        pygame.draw.rect(screen, pygame.Color('blue'), fruit_rect)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def draw_main(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def collision(self):
        if self.snake.body[0] == self.fruit.fruit_pos:
            # code
            print("Collision is happened")


pygame.init()

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()

main = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.snake.move_snake()
            main.collision()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                main.snake.direction = Vector2(1, 0)
        # Draw all our elements
    screen.fill((0, 0, 0))
    main.draw_main()

    pygame.display.update()
    clock.tick(60)
