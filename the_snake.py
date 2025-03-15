import sys
from random import randint
import pygame
import logging

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
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
SPEED = 15


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инициализирует объект GameObject.

        Args:
            position (tuple): Позиция объекта на игровом поле).
            body_color (tuple): Цвет объекта в формате RGB.
        """
        self.position = position  # Позиция объекта
        self.body_color = body_color  # Цвет объекта

    def draw(self, screen):
        """Метод для отрисовки объекта на экране.
        Этот метод должен быть реализован в дочерних классах.
        """
        raise NotImplementedError("Метод 'draw' должен быть реализован в дочернем классе.")

    def update(self):
        """Метод для обновления состояния объекта.
        Может быть переопределен в дочерних классах.
        """
        pass  # Можно оставить пустым, если не требуется обновления

    def set_position(self, position):
        """Устанавливает новую позицию объекта.

        Args:
            position (tuple): Новая позиция объекта.
        """
        self.position = position

    def get_position(self):
        """Возвращает текущую позицию объекта.

        Returns:
            tuple: текущая позиция объекта.
        """
        return self.position

    def set_color(self, color):
        """Устанавливает новый цвет объекта.

        Args:
            color (tuple): Новый цвет в формате RGB.
        """
        self.body_color = color

    def get_color(self):
        """Возвращает текущий цвет объекта.

        Returns:
            tuple: текущий цвет объекта.
        """
        return self.body_color

def random_position(excluded_positions):
    """Generate a random position not in the excluded positions."""
    while True:
        position = (randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1))
        if position not in excluded_positions:
            return position

class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.apple_count = 0  # Счётчик съеденных яблок.

    def update(self):
        """Обновить положение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Проверка на выход за границы и телепортация.
        new_head = (
            new_head[0] % GRID_WIDTH,
            new_head[1] % GRID_HEIGHT
        )

        # Проверка на столкновение с телом.
        if new_head in self.positions[1:]:
            return True  # Столкновение с самим собой.

        self.positions.insert(0, new_head)  # Добавляем новую голову
        self.positions.pop()  # Удаляем хвост
        return False  # Нет столкновения.

    def grow(self):
        """Увеличить длину змейки."""
        self.apple_count += 1
        self.positions.append(self.positions[-1])  # Добавляем сегмент в хвост

    def draw(self, screen):
        """Отрисовать змейку на экране."""
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
    """Яблоко."""

    def __init__(self):
        self.position = None
        self.body_color = APPLE_COLOR

    def random_position(self, excluded_positions):
        """Сгенерировать случайное положение для яблока."""
        self.position = random_position(excluded_positions)

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
    """Препятствие (камень)."""

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
            sys.exit()  # Завершение игры.
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
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    logging.basicConfig(level=logging.INFO)

    # Создаем экземпляры классов.
    snake = Snake()
    apple = Apple()
    apple.random_position(snake.positions)  # Генерируем позицию яблока.
    stones = []

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.update():  # Проверяем на столкновение с самим собой.
            logging.info('Игра окончена! Змея столкнулась сама с собой.')
            break

        # Проверка на столкновение со яблоком
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.random_position(
                snake.positions + [stone.position for stone in stones]
            )
            # Добавляем проверку на появление камней
            if snake.apple_count % 5 == 0:  # Каждые 5 съеденных яблок
                new_stone_position = random_position(
                    snake.positions + [apple.position] +
                    [stone.position for stone in stones]
                )
                stones.append(Stone(new_stone_position))

        # Проверка на столкновение с камнями
        if snake.positions[0] in [stone.position for stone in stones]:
            logging.info('Игра окончена! Змея столкнулась с камнем.')
            break

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        for stone in stones:
            stone.draw(screen)  # Отрисовка камней
        snake.draw(screen)
        pygame.display.flip()

    pygame.quit()  # Завершение игры


if __name__ == '__main__':
    main()
