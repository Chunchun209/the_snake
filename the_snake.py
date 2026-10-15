from random import randint
import sys

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь с направлениями движения: ключ — нажатая клавиша.
TURNS = {
    pg.K_UP: (UP, DOWN),
    pg.K_DOWN: (DOWN, UP),
    pg.K_LEFT: (LEFT, RIGHT),
    pg.K_RIGHT: (RIGHT, LEFT),
}


# Базовые цвета:
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (93, 216, 228)

# Константы игры:
BOARD_BACKGROUND_COLOR = BLACK
BORDER_COLOR = BLUE
APPLE_COLOR = RED
SNAKE_COLOR = GREEN

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех объектов игры."""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        """Инициализирует базовые атрибуты игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки объектов на игровом поле."""
        pass

    def draw_cell(self, position, color=None):
        """Вспомогательный метод для отрисовки одной ячейки на поле."""
        if color is None:
            color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        if color == BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)
        else:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и поведение яблока на игровом поле."""

    def __init__(self, occupied_cells=None):
        """Инициализирует яблоко, задает цвет и случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """Метод для выбора случайного места появления яблока."""
        if occupied_cells is None:
            occupied_cells = []

        while True:
            x = randint(0, (GRID_WIDTH - 1)) * GRID_SIZE
            y = randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
            new_position = (x, y)
            if new_position not in occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Метод для отрисовки яблока на иговом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку и поведение змейки на игровом поле."""

    def __init__(self):
        """Инициализирует начальное состояние и параметры змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Метод для изменения направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод для вычисления координат головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки на игровом поле.

        Добавляет новую голову в начало списка координат, обрабатывает
        прохождение змейки через границу поля и удаляет последний сегмент
        тела, если она не выросла.
        """
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_head_x, new_head_y)
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает игру в начальное состояние.

        Вызывается при столкновении змейки с самой собой для обнуления
        всех параметров тела и направления к дефолтным значениям.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод, отрисовывающий змейку."""
        for position in self.positions[:-1]:
            self.draw_cell(position)
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, color=BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция, обрабатывающая нажатие клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            elif event.key in TURNS:
                new_direction, opposite = TURNS[event.key]
                if game_object.direction != opposite:
                    game_object.next_direction = new_direction


def main():
    """Функция, управляющая всем игровым процессом."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
