import random
import sys

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
SPEED = 10

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализирует объект с заданной позицией."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на поверхности."""
        raise NotImplementedError('Метод draw должен быть переопределен.')


class Apple(GameObject):
    """Класс для яблока, которое может съесть змейка."""

    def __init__(
        self,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        grid_size=GRID_SIZE
    ):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        x = (random.randint(0, self.screen_width // self.grid_size - 1)
             * self.grid_size)
        y = (random.randint(0, self.screen_height // self.grid_size - 1)
             * self.grid_size)
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на поверхности."""
        rect = pygame.Rect(self.position, (self.grid_size, self.grid_size))
        pygame.draw.rect(surface, APPLE_COLOR, rect)


class Snake(GameObject):
    """Класс для змейки, управляемой игроком."""

    def __init__(
        self,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        grid_size=GRID_SIZE
    ):
        """Инициализирует змейку в центре экрана."""
        center_x = ((screen_width // 2) // grid_size) * grid_size
        center_y = ((screen_height // 2) // grid_size) * grid_size
        super().__init__((center_x, center_y), body_color=SNAKE_COLOR)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.grid_size = grid_size
        self.direction = (0, 0)
        self.positions = [self.position]
        self.length = 1
        self.last = None
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки."""
        current_head = self.get_head_position()
        dx, dy = self.direction
        new_x = (current_head[0] + dx * self.grid_size) % self.screen_width
        new_y = (current_head[1] + dy * self.grid_size) % self.screen_height
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на поверхности."""
        for position in self.positions:
            rect = pygame.Rect(position, (self.grid_size, self.grid_size))
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

    def update_direction(self, key):
        """Обрабатывает ввод пользователя."""
        new_dir = None
        if key == pygame.K_UP:
            new_dir = (0, -1)
        elif key == pygame.K_DOWN:
            new_dir = (0, 1)
        elif key == pygame.K_LEFT:
            new_dir = (-1, 0)
        elif key == pygame.K_RIGHT:
            new_dir = (1, 0)

        if new_dir is not None:
            current_dir = self.direction
            if (new_dir[0] != -current_dir[0]
                    or new_dir[1] != -current_dir[1]):
                self.direction = new_dir


def handle_keys(snake):
    """Обрабатывает события ввода с клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            snake.update_direction(event.key)
    return True


def main(test_mode=False):
    """Основная функция, запускающая игру."""
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Snake Game')

    snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE)

    snake = Snake()
    apple = Apple()

    running = True
    frame_count = 0

    while running:
        running = handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()
        clock.tick(SPEED)

        # В тестовом режиме завершаем игру после 10 кадров
        if test_mode:
            frame_count += 1
            if frame_count >= 10:
                running = False


if __name__ == '__main__':
    main()
