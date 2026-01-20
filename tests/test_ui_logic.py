import pytest
import conftest # Sets up paths and mocks
from unittest.mock import MagicMock
from ui import Score, Menu

def test_score_increment():
    """Testa se a propriedade score incrementa corretamente e é reativa."""
    score_obj = Score()
    initial_text = score_obj.text
    score_obj.score += 10
    assert score_obj.score == 10
    assert score_obj.text != initial_text
    assert "10" in score_obj.text

def test_menu_navigation():
    """Testa a lógica de navegação circular do menu."""
    options = [["Opt1", lambda: None], ["Opt2", lambda: None], ["Opt3", lambda: None]]
    menu = Menu(*options)
    
    assert menu.option == 0
    
    # Próxima opção
    menu.option += 1
    assert menu.option == 1
    
    # Wrap around (forward)
    menu.option = 2
    menu.option += 1
    assert menu.option == 0
    
    # Wrap around (backward)
    menu.option = 0
    menu.option -= 1
    assert menu.option == 2

def test_menu_callback():
    """Verifica se o callback da opção do menu é chamado via mock."""
    callback = MagicMock()
    options = [["Opt1", callback]]
    menu = Menu(*options)
    
    # Simula evento de teclado ENTER
    import pygame
    mock_event = MagicMock()
    mock_event.type = pygame.KEYDOWN
    mock_event.key = pygame.K_RETURN
    
    menu.update([mock_event])
    callback.assert_called_once()
