import pygame
import random
import os

def GetFile(name: str):
    return os.path.dirname(__file__) + '/' + name

num_cells = 15
screen_size = width, height = 450, 450
cell_size = cell_width, cell_height = width / num_cells, height / num_cells
snake = [(5, 5)]
direction = (0, 1)
apple = (2, 1)
score = 0
fps = 10
snake_head = pygame.image.load(GetFile("snake head.png"))
snake_head = pygame.transform.scale(snake_head, (cell_width - 2, cell_height - 2))
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake!")

def move_apple(snake, num_cells):
    while True:
        new_apple_x = random.randint(0, num_cells - 1)
        new_apple_y = random.randint(0, num_cells - 1)
        
        if (new_apple_x, new_apple_y) not in snake:
            return new_apple_x, new_apple_y
        
def hit_apple(apple, snake):
    if snake[-1] == apple:
        return True
    return False

def self_collision(snake):
    if len(snake) != 1:
        return snake[-1] in snake[:-1]
    return False

def draw_board(screen, screen_size, cell_width, cell_height, width, height):
    screen.fill("white")
    for i in range(width):
        pygame.draw.line(screen, "black",
                         (i * cell_width, 0), (i * cell_width, height), 1)
        pygame.draw.line(screen, "black", 
                         (0, i * cell_height), (width, i * cell_height), 1)

def draw_snake(screen, snake, cell_width, cell_height, direction):
    dir_to_angle = {(-1, 0): -90, (1, 0): 90, (0, -1): 180, (0, 1): 0}
    screen.blit(
        pygame.transform.rotate(snake_head, dir_to_angle[direction]),
        (snake[-1][0] * cell_width + 1, snake[-1][1] * cell_width + 1))
    for t in snake[:-1]:
        pygame.draw.rect(screen, (110, 190, 50),
                         (t[0] * cell_width, t[1] * cell_height,
                          cell_width, cell_height))

def draw_apple(screen, apple, cell_width, cell_height):
    image = pygame.image.load(GetFile("picture of apple.webp"))
    image = pygame.transform.scale(image, (cell_width - 2, cell_height - 2))
    screen.blit(image, (apple[0] * cell_width + 1, apple[1] * cell_height + 1))

def move_snake(snake, direction, num_cells):
    snake_head_x, snake_head_y = snake[-1]
    new_head_x = (snake_head_x + direction[0]) % num_cells
    new_head_y = (snake_head_y + direction[1]) % num_cells
    new_head = (new_head_x, new_head_y)
    snake.append(new_head)

draw_board(screen, num_cells, cell_width, cell_height, width, height)
draw_snake(screen, snake, cell_width, cell_height, direction)
draw_apple(screen, apple, cell_width, cell_height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            if event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
    move_snake(snake, direction, num_cells)
    if hit_apple(apple, snake):
        score += 1
        print("Score: %d" % score)
        print(len(snake))
        apple = move_apple(snake, num_cells)
    else:
        snake.pop(0)
    
    if self_collision(snake):
        print("Game over! Final score: %d" % score)
        pygame.quit()
        exit(0)
    
    draw_board(screen, screen_size, cell_width, cell_height, width, height)
    draw_apple(screen, apple, cell_width, cell_height)
    draw_snake(screen, snake, cell_width, cell_height, direction)
    pygame.display.update()
    clock.tick(fps)