import os
import random
import asyncio
import pygame
import sys
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [ Vector2(4, 10), Vector2(3, 10), Vector2(2, 10), Vector2(1, 10) ]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                pygame.draw.rect(screen, (0, 0, 0), block_rect)
            else:
                pygame.draw.rect(screen, (251, 198, 207), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[ : ]
            body_copy.insert(0, body_copy[ 0 ] + self.direction)
            self.body = body_copy[ : ]
            self.new_block = False
        else:
            body_copy = self.body[ :-1 ]
            body_copy.insert(0, body_copy[ 0 ] + self.direction)
            self.body = body_copy[ : ]

    def add_block(self):
        self.new_block = True


def random_pos():
    x = random.randint(0, cell_number - 1) * cell_size
    y = random.randint(0, cell_number - 1) * cell_size
    return x, y


def target_fruit():
    return random.randint(0, 2)

# generate index for theme in fruit class
def random_theme():
    return random.randint(0, 1)

class Fruit:

    # categories theme
    # fruit_target
    # fetch the text and path from json
    # display graphics whereas the text in the middle of the screen
    # if target fruit hit, the score increase

    def __init__(self):
        self.text_surface = None
        self.target_fruit = target_fruit()
        self.fruit_pos = [ Vector2(random_pos()), Vector2(random_pos()), Vector2(random_pos()) ]
        self.apple = pygame.image.load(os.path.join("Graphics", "apple.png"))
        self.banana = pygame.image.load(os.path.join("Graphics", "banana.png"))
        self.coconet = pygame.image.load(os.path.join("Graphics", "coconet.png"))
        self.orange = pygame.image.load(os.path.join("Graphics", "orange.png"))
        self.pineapple = pygame.image.load(os.path.join("Graphics", "pineapple.png"))
        self.water_melon = pygame.image.load(os.path.join("Graphics", "water_melon.png"))
        self.fruit_theme1 = [ {"text": "Apple", "image": self.apple},
                              {"text": "Banana", "image": self.banana},
                              {"text": "Coconet", "image": self.coconet} ]
        self.fruit_theme2 = [ {"text": "Orange", "image": self.orange},
                              {"text": "Pineapple", "image": self.pineapple},
                              {"text": "Water Melon", "image": self.water_melon} ]
        self.theme = [
            {
                "theme": self.fruit_theme1,
                "complete": False,
            }, {
                "theme": self.fruit_theme2,
                "complete": False,
            }
        ]
        # randomize theme -> display select theme

        # error - there is 2 themes, so after two correctness, the target range will out of bounces
        self.target_theme = random_theme()


        # need to apple two fruits that unknown

    def draw_fruit(self):
        font = pygame.font.SysFont("comics", 30)

        if self.theme[self.target_theme]['complete']:
            self.target_theme = random_theme()
        else:
            theme = self.theme[self.target_theme]['theme']
        for index, block in enumerate(self.fruit_pos):
            fruit_data = theme[index % len(theme)]
            resized_image = pygame.transform.scale(fruit_data['image'], (cell_size + 5, cell_size + 5))
            screen.blit(resized_image, (int(block.x), int(block.y)))

        fruit_text = ''
        for index, block in enumerate(theme):
            if index == game.fruit.target_fruit:
                fruit_text = block[ 'text' ]
        self.text_surface = font.render(f"Find {fruit_text}", True, (0, 0, 0))


class Game:
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
        if not 0 <= self.snake.body[ 0 ].x < cell_number or not 0 <= self.snake.body[ 0 ].y < cell_number:
            self.game_over()

        for blocks in self.snake.body[ 1: ]:
            if blocks == self.snake.body[ 0 ]:
                self.game_over()

    def draw_main(self):
        self.map.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        screen.blit(self.fruit.text_surface, (900 // 2, 100 // 2))

    def collision(self):
        target_pos = self.fruit.fruit_pos[ self.fruit.target_fruit ]
        snake_head = self.snake.body[ 0 ] * cell_size

        # snake head and target fruit collision check
        if snake_head == target_pos:
            self.fruit.theme[self.fruit.target_theme]['complete'] = True
            self.fruit.target_theme = random_theme()
            self.snake.add_block()
            # Respawn a new target fruit position
            self.fruit.target_fruit = target_fruit()

            # Reposition fruits
            self.fruit.fruit_pos = [ Vector2(random_pos()), Vector2(random_pos()), Vector2(random_pos()) ]

        # check between snake head is hitting other fruits which is not target fruit
        for fruits in self.fruit.fruit_pos:
            if fruits != target_pos and snake_head == fruits:
                self.game_over()

pygame.init()

cell_size = 24
cell_number = 24

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
pygame.display.set_caption("Welcome to Snake game!")

game = Game()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)

async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over()

            if event.type == SCREEN_UPDATE:
                game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if game.snake.direction.y != 1:
                        game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if game.snake.direction.y != -1:
                        game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if game.snake.direction.x != 1:
                        game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if game.snake.direction.x != -1:
                        game.snake.direction = Vector2(1, 0)

        # Draw all our elements
        screen.fill(game.map.grass_color2)

        game.draw_main()
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())