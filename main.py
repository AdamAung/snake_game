import pygame, sys
from pygame.math import Vector2
import random

class Snake:
    def __init__(self):
        self.body = [Vector2(3, 10), Vector2(2, 10), Vector2(1, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

def random_pos():
    x = random.randint(0, cell_number - 1 ) * cell_size
    y = random.randint(0, cell_number - 1) * cell_size
    return x, y

def target_fruit():
    return random.randint(0, 2)

class Fruit:
    def __init__(self):
        self.target_fruit = target_fruit()
        self.fruit_pos = [Vector2(random_pos()), Vector2(random_pos()), Vector2(random_pos())]


    def draw_fruit(self):
        for block in self.fruit_pos:
            fruit_rect = pygame.Rect(int(block.x), int(block.y), cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color('blue'), fruit_rect)

class Map:
    def __init__(self):
        pass

    # Need to add map layouts graphics

    # Need to add Snake graphics

    # Need to add Fruits graphics

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        

    def game_over(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.check_fail()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for blocks in self.snake.body[1:]:
            if blocks == self.snake.body[0]:
                self.game_over()

    def draw_main(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def collision(self):
        target_pos = self.fruit.fruit_pos[self.fruit.target_fruit]
        snake_head = self.snake.body[0] * cell_size

        # snake head and target fruit collision check
        if snake_head == target_pos:
            self.snake.add_block()
            # Respawn a new target fruit position
            self.fruit.target_fruit = target_fruit()
            # Reposition fruits
            self.fruit.fruit_pos = [Vector2(random_pos()), Vector2(random_pos()), Vector2(random_pos())]


        # check between snake head is hitting other fruits which is not target fruit
        for fruits in self.fruit.fruit_pos:
            if fruits != target_pos and snake_head == fruits:
                self.game_over()

pygame.init()

cell_size = 10
cell_number = 90

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
pygame.display.set_caption("Welcome to Snake game!")

font = pygame.font.SysFont("comics", 30)

main = Main()

text_surface = font.render(main.text.text, True, pygame.Color("Red"))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main.game_over()

        if event.type == SCREEN_UPDATE:
            main.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)

    # Draw all our elements
    screen.fill((0, 0, 0))
    main.draw_main()
    pygame.display.update()
    clock.tick(60)
