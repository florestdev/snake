# -*- coding: utf-8 -*-
from os import environ, system
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
try:
  import pygame
  from colorama import Fore
except ImportError:
  system('pip install pygame')
  system('pip install colorama')
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
#screen_width = 600
#screen_height = 600
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Змейка от Florest.")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Размер клетки
cell_size = 20

# Направление движения змейки
direction = 'right'

# Список для хранения позиций змейки
snake_body = [pygame.Rect(cell_size, cell_size, cell_size, cell_size), 
              pygame.Rect(cell_size * 2, cell_size, cell_size, cell_size)]

# Скорость движения змейки
clock = pygame.time.Clock()

# Переменные для яблока
apple = None  # Объявим apple здесь
def generate_apple():
    global apple
    while True:
        apple_x = random.randrange(0, screen_width // cell_size) * cell_size
        apple_y = random.randrange(0, screen_height // cell_size) * cell_size
        apple = pygame.Rect(apple_x, apple_y, cell_size, cell_size)
        if not any(apple.colliderect(segment) for segment in snake_body):
           break
generate_apple()

# Переменные для счета
score = 0
font = pygame.font.Font(None, 36)

print(f'{Fore.GREEN}Игра началась. Удачи!')
# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == ord('w'):
                if direction != 'down':
                    direction = 'up'
            elif event.key == pygame.K_s or event.key == ord('s'):
                if direction != 'up':
                    direction = 'down'
            elif event.key == pygame.K_a or event.key == ord('a'):
                if direction != 'right':
                    direction = 'left'
            elif event.key == pygame.K_d or event.key == ord('d'):
                if direction != 'left':
                   direction = 'right'
            elif event.key == pygame.K_ESCAPE:
                running = False
            else:
                pass

    # Обновление направления змейки
    if direction == 'right':
        new_head = pygame.Rect(snake_body[0].x + cell_size, snake_body[0].y, cell_size, cell_size)
    elif direction == 'left':
        new_head = pygame.Rect(snake_body[0].x - cell_size, snake_body[0].y, cell_size, cell_size)
    elif direction == 'up':
        new_head = pygame.Rect(snake_body[0].x, snake_body[0].y - cell_size, cell_size, cell_size)
    elif direction == 'down':
        new_head = pygame.Rect(snake_body[0].x, snake_body[0].y + cell_size, cell_size, cell_size)

    snake_body.insert(0,new_head)

    # Проверка столкновения с яблоком
    if snake_body[0].colliderect(apple):
      score += 1
      generate_apple()
      print(f'{Fore.YELLOW}Так держать! Продолжай.')
    else:
      snake_body.pop()


    # Проверка столкновения змейки с собой
    for segment in snake_body[1:]:
        if segment == snake_body[0]:
            running = False

    # Проверка столкновения змейки с границами экрана
    if snake_body[0].x < 0 or snake_body[0].x >= screen_width or snake_body[0].y < 0 or snake_body[0].y >= screen_height:
        running = False

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование змейки
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, segment)

    # Рисование яблока
    pygame.draw.rect(screen, RED, apple)
    
    # Отображение счета
    text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    text2 = font.render('esc - выход.', True, WHITE)
    screen.blit(text2, (10,40))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(10)
pygame.quit()
print(f'{Fore.RED}Игра окончена. Вы проиграли со счетом {score}.')
sys.exit()
