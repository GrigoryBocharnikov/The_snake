from unittest.mock import patch
import pytest
import pygame

def test_main_run_without_exceptions(_the_snake):
    with patch.object(pygame.event, 'get') as mock_event_get:
        # Имитируем событие выхода после первого кадра
        mock_event_get.side_effect = [
            [pygame.event.Event(pygame.QUIT)],
            []
        ]
        with patch.object(pygame, 'quit'):
            _the_snake.main()
