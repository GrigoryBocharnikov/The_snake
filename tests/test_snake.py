import pytest

from the_snake import Snake


@pytest.fixture
def snake():
    return Snake()


def test_snake_initial_position(snake):
    assert snake.positions == [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]


def test_snake_movement():
    snake = Snake()
    initial_head = snake.positions[0]
    snake.next_direction = RIGHT
    snake.update()
    new_head = (initial_head[0] + 1, initial_head[1])
    assert snake.positions[0] == new_head
