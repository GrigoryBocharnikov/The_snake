# Стандартные библиотеки
import logging
import sys
from random import randint

# Сторонние библиотеки
import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки
SPEED = 15


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инницифлизирует обьект GameObject.
        Args:
            position (typle): Позиция обекта на игровом поле).
            body_color (tuple): Цветобьекта в формате RGB.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Метод для отрисовки обьекта на экране.
        Этот метод должен быть реализован в дочерних классах.
        """
        raise NotImplementedError(
            "Метод 'draw' должен быть реализован в дочернем классе."
        )

    def update(self):
        """Метод для обновления состояния обьекта.
        Может быть переопределен в дочерних классах.
        """
        pass

    def set_position(self, position):
        """Устанавливает новую позицию обьекта.
        Args:
            position (tuple): Новая позиция обьекта.
        """
        self.position = position

    def get_position(self):
        """Возвращает текущию позицию обьекта."""
        return self.position

    def set_color(self, color):
        """Устанавливает новый цвет обьекта.
        Args:
            color (tuple): Новый цвет в формате RGB.
        """
        self.body_color = color

    def get_color(self):
        """Возвращает текущий цвет обьекта.
        Returns:
            tuple: Текущий цвет обьекта.
        """
        return self.body_color


def generate_random_position(excluded_positions):
    """Генерирует позицию, не входящую в excluded_positions."""
    while True:
        position = (randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1))
        if position not in excluded_positions:
            return position


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.apple_count = 1

    def update(self):
        """Обновить положение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in self.positions[1:]:
            return True

        self.positions.insert(0, new_head)
        self.positions.pop()
        return False

    def grow(self):
        """Увеличеть длину змейки."""
        self.apple_count += 1
        self.positions.append(self.positions[-1])

    def draw(self, screen):
        """отрисовать змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        self.position = None
        self.body_color = APPLE_COLOR

    def random_position(self, excluded_positions):
        """Сгенерировать случайное положение для яблока."""
        self.position = generate_random_position(excluded_positions)

    def draw(self, screen):
        """Отрисовать яблоко на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс камня."""

    def __init__(self, position):
        self.position = position
        self.body_color = STONE_COLOR

    def draw(self, screen):
        """Отрисовать камень на экране."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Обработать нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    logging.basicConfig(level=logging.INFO)

    snake = Snake()
    apple = Apple()
    apple.random_position(snake.positions)
    stones = []

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.update():
            logging.error('Игра окончена! Змея столкнулась сама с собой.')
            break

        if snake.positions[0] == apple.position:
            snake.grow()
            excluded = snake.positions + [stone.position for stone in stones]
            apple.random_position(excluded)

            if snake.apple_count % 5 == 0:
                new_stone_position = generate_random_position(
                    excluded + [apple.position]
                )
                stones.append(Stone(new_stone_position))

        if snake.positions[0] in [stone.position for stone in stones]:
            logging.error('Игра окончена! Змея столкнулась с камнем.')
            break

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        for stone in stones:
            stone.draw(screen)
        snake.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
