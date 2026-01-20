import pytest
import conftest # Sets up paths and mocks
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GREEN, BLACK

def test_screen_dimensions():
    """Valida as dimensões da tela."""
    assert SCREEN_WIDTH > 0
    assert SCREEN_HEIGHT > 0
    assert isinstance(SCREEN_WIDTH, int)
    assert isinstance(SCREEN_HEIGHT, int)

def test_fps_limit():
    """Garante que o FPS está em um intervalo razoável."""
    assert 10 <= FPS <= 120

def test_colors_format():
    """Valida se as cores estão no formato RGB (tuplas de 3)."""
    for color in [GREEN, BLACK]:
        assert isinstance(color, tuple)
        assert len(color) == 3
        for component in color:
            assert 0 <= component <= 255
