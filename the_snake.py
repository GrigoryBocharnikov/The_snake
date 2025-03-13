import sys
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

"""Направления движения."""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (128, 128, 128)  # Цвет камня.

# Скорость движения змейки:
SPEED = 5


class GameObject:
    """Базовый класс для игровых объектов.

    Attributes:
        position (tuple): Позиция объекта на игровом поле.
        body_color (tuple): Цвет тела объекта.
    """

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализирует объект GameObject.

        Args:
            position (tuple): Начальная позиция объекта.
            body_color (tuple): Цвет тела объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Метод для отрисовки объекта на экране."""
        pass  # Реализуйте в дочерних классах


def random_position(excluded_positions):
    """Генератор случайной позиции для объекта.

    Args:
        excluded_positions (list): Список позиций, которые следует избегать.

    Returns:
        tuple: Случайная позиция, не входящая в excluded_positions.
    """
    while True:
        position = (randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1))
        if position not in excluded_positions:
            return position


class Snake(GameObject):
    """Механизм отрисовки и стирания Змейки.

    Attributes:
        positions (list): Список позиций сегментов змеи.
        direction (tuple): Текущее направление движения.
        next_direction (tuple): Направление, в которое змейка должна двигаться.
    """

    def __init__(self):
        """Инициализирует объект Snake."""
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.apple_count = 0  # Счётчик съеденных яблок.

    def update(self) -> bool:
        """Обновляет позицию змеи.

        Returns:
            bool: True, если змейка столкнулась сама с собой, иначе False.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Проверка на выход за границы и телепортация.
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)

        # Проверка на столкновение с телом.
        if len(self.positions) >= 5 and new_head in self.positions[1:]:
            return True  # Столкновение с самим собой.

        self.last = self.positions[-1]
        self.positions = [new_head] + self.positions[:-1]
        return False  # Нет столкновения.

    def grow(self):
        """Увеличивает длину змеи при поедании яблока."""
        self.apple_count += 1
        self.positions.append(self.last)

    def draw(self, screen):
        """Отрисовывает змею на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы.
        head_rect = pygame.Rect(
            self.positions[0][0] * GRID_SIZE,
            self.positions[0][1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змеи.

        Returns:
            tuple: Позиция головы.
        """
        return self.positions[0]

    def move(self):
        """Логика движения змеи (пока не реализована)."""
        pass

    def reset(self):
        """Сбрасывает состояние змеи (пока не реализовано)."""
        pass
    def update_direction(self, new_direction):

        """Обновляет направление змеи, если новое направление не противоположно текущему."""
        if ((new_direction[0] * -1,
            new_direction[1] * -1) != self.direction):
            self.next_direction = new_direction


class Apple(GameObject):
    """Механизм отрисовки и стирания Яблоко."""

    def __init__(self):
        """Инициализирует объект Apple."""
        super().__init__()  # Вызов конструктора родительского класса
        self.randomize_position()  # Сразу рандомизируем позицию при создании

    def randomize_position(self, excluded_positions=None):
        """Проверка позиции.

        Args:
            excluded_positions (list): Список позиций, которые следует избегать.
        """
        if excluded_positions is None:
            excluded_positions = []
        self.position = random_position(excluded_positions)

    def draw(self, screen):
        """Метод для отрисовки объекта на экране."""

        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, APPLE_COLOR, rect, 20)


class Stone(GameObject):
    """Механизм отрисовки и стирания Stone."""

    def __init__(self, position):
        """Инициализирует объект Stone.

        Args:
            position (tuple): Позиция камня на игровом поле.
        """
        super().__init__(position=position, body_color=STONE_COLOR)

    @staticmethod
    def random_position(excluded_positions):
        """Проверка позиции на наличие других объектов.
        Args:
            excluded_positions (list): Список позиций, которые следует избегать.
        Returns:
            tuple: Случайная позиция, не входящая в excluded_positions.
        """
        return random_position(excluded_positions)

    def draw(self, screen):
        """Метод для отрисовки объекта на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Основные механизмы игры и змейки.

    Args:
        game_object (GameObject): Объект игры для обработки управления.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Завершение игры.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame."""
    pygame
