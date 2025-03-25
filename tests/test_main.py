from unittest.mock import patch, MagicMock
import pytest

def test_main_run_without_exceptions():
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.time.Clock') as mock_clock, \
         patch('pygame.event.get') as mock_event_get:

        # Настраиваем моковые объекты
        mock_clock_instance = MagicMock()
        mock_clock.return_value = mock_clock_instance
        mock_event_get.return_value = [MagicMock(type=pygame.QUIT)]

        # Запускаем в тестовом режиме
        from the_snake import main
        main(test_mode=True)
